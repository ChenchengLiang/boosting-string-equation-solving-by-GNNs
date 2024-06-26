from src.solver.independent_utils import strip_file_name_suffix, dump_to_json_with_format
from src.solver.Parser import Parser, EqParser
import glob
from src.solver.utils import graph_func_map
from typing import List, Tuple, Dict, Union, Optional, Callable
import os
import shutil
import json
from src.solver.Constants import satisfiability_to_int_label, UNKNOWN
from src.solver.DataTypes import Equation, Edge,Terminal,Term,SeparateSymbol
from src.solver.algorithms.utils import merge_graphs,graph_to_gnn_format,concatenate_eqs
from src.solver.visualize_util import draw_graph
import zipfile
import fnmatch
from tqdm import tqdm



def dvivde_track_for_cluster(benchmark, file_folder="ALL",chunk_size=50):
    folder = benchmark + "/"+file_folder
    chunk_size = chunk_size

    folder_counter = 0
    all_folder = folder + "/ALL"
    if not os.path.exists(all_folder):
        os.mkdir(all_folder)

    for file in glob.glob(folder + "/*"):
        shutil.move(file, all_folder)

    for i, eq_file in enumerate(glob.glob(all_folder + "/*.eq")):
        if i % chunk_size == 0:
            folder_counter += 1
            divided_folder_name = folder + "/divided_" + str(folder_counter)
            os.mkdir(divided_folder_name)
        file_name = strip_file_name_suffix(eq_file)
        for f in glob.glob(file_name + ".eq") + glob.glob(file_name + ".answer") + glob.glob(file_name + ".smt2"):
            shutil.copy(f, divided_folder_name)


def _read_label_and_eqs(zip,f,graph_folder,parser,graph_func):
    with zip.open(f) as json_file:
    #with open(f, 'r') as json_file:
        json_dict = json.loads(json_file.read())
    file_name = f.replace(".label.json", "")


    eq_file = file_name + ".eq"
    #split_eq_file_list = [graph_folder + "/" + x for x in json_dict["middle_branch_eq_file_name_list"]]
    split_eq_file_list = ["train/" + x for x in json_dict["middle_branch_eq_file_name_list"]]

    eq:Equation=concatenate_eqs(parser.parse(eq_file,zip)["equation_list"])
    #print("eq",len(eq.eq_str),eq.eq_str)
    eq_nodes, eq_edges = graph_func(eq.left_terms, eq.right_terms)
    split_eq_list: List[Equation] = [concatenate_eqs(parser.parse(split_eq_file,zip)["equation_list"]) for split_eq_file in
                                     split_eq_file_list]
    return eq_nodes,eq_edges,split_eq_list, split_eq_file_list, json_dict["label_list"],json_dict["satisfiability_list"]

def _read_label_and_eqs_for_rank(zip,f,parser):
    with zip.open(f) as json_file:
        json_dict = json.loads(json_file.read())

    rank_eq_file_list = ["train/" + x for x in json_dict["middle_branch_eq_file_name_list"]]

    split_eq_list: List[Equation] = [concatenate_eqs(parser.parse(split_eq_file,zip)["equation_list"]) for split_eq_file in
                                     rank_eq_file_list]
    return split_eq_list, rank_eq_file_list, json_dict["label_list"],json_dict["satisfiability_list"]




def output_rank_eq_graphs(zip_file:str,graph_folder: str, graph_func: Callable, visualize: bool = False):
    parser = get_parser()
    with zipfile.ZipFile(zip_file, 'r') as zip_file_content:
        for f in tqdm(zip_file_content.namelist(),desc="output_rank_eq_graphs"): #scan all files in zip
            if fnmatch.fnmatch(f, '*.label.json'):
                rank_eq_list, rank_eq_file_list, label_list, satisfiability_list = _read_label_and_eqs_for_rank(
                    zip_file_content, f, parser)
                multi_graph_dict = {}
                for i,(split_eq, split_file, split_label,split_satisfiability) in enumerate(zip(rank_eq_list, rank_eq_file_list, label_list,satisfiability_list)):
                    split_eq_nodes, split_eq_edges = graph_func(split_eq.left_terms, split_eq.right_terms)

                    if visualize == True:
                        draw_graph(nodes=split_eq_nodes, edges=split_eq_edges, filename=split_file)

                    graph_dict = graph_to_gnn_format(split_eq_nodes, split_eq_edges, label=split_label,satisfiability=split_satisfiability)
                    multi_graph_dict[i]=graph_dict
                # Dumping the dictionary to a JSON file
                json_file = graph_folder + "/" + f.replace(".label.json", ".graph.json").replace("train/", "")
                dump_to_json_with_format(multi_graph_dict, json_file)

def output_split_eq_graphs(zip_file:str,graph_folder: str, graph_func: Callable, visualize: bool = False):
    parser = get_parser()
    with zipfile.ZipFile(zip_file, 'r') as zip_file_content:
        for f in tqdm(zip_file_content.namelist(),desc="output_split_eq_graphs"):
        #for f in glob.glob(graph_folder + "/*.label.json"):
            if fnmatch.fnmatch(f, '*.label.json'):
                eq_nodes, eq_edges, split_eq_list, split_eq_file_list, label_list,satisfiability_list = _read_label_and_eqs(zip_file_content,f, graph_folder, parser,
                                                                                                    graph_func)
                multi_graph_dict={}
                #get parent eq graph
                graph_dict = graph_to_gnn_format(eq_nodes, eq_edges, label=-1,
                                                 satisfiability=UNKNOWN)
                multi_graph_dict[0]=graph_dict

                for i,(split_eq, split_file, split_label,split_satisfiability) in enumerate(zip(split_eq_list, split_eq_file_list, label_list,satisfiability_list)):
                    split_eq_nodes, split_eq_edges = graph_func(split_eq.left_terms, split_eq.right_terms)

                    if visualize == True:
                        merged_nodes, merged_edges = merge_graphs(eq_nodes, eq_edges, split_eq_nodes, split_eq_edges)
                        draw_graph(nodes=merged_nodes, edges=merged_edges, filename=split_file)

                    graph_dict = graph_to_gnn_format(split_eq_nodes, split_eq_edges, label=split_label,satisfiability=split_satisfiability)
                    multi_graph_dict[i+1]=graph_dict

                # Dumping the dictionary to a JSON file
                json_file = graph_folder+"/"+f.replace(".label.json",".graph.json").replace("train/","")
                dump_to_json_with_format(multi_graph_dict, json_file)


def output_pair_eq_graphs(zip_file:str,graph_folder: str, graph_func: Callable, visualize: bool = False):
    parser = get_parser()

    with zipfile.ZipFile(zip_file, 'r') as zip_file_content:
        for f in zip_file_content.namelist():
            if fnmatch.fnmatch(f, '*.label.json'):
                eq_nodes,eq_edges,split_eq_list, split_eq_file_list, label_list,satisfiability_list=_read_label_and_eqs(zip_file_content,f, graph_folder, parser, graph_func)

                #print("eq", eq.eq_str)
                for split_eq, split_file, split_label,split_satisfiability in zip(split_eq_list, split_eq_file_list, label_list,satisfiability_list):
                    #print("split_eq", split_eq.eq_str)
                    split_eq_odes, split_eq_edges = graph_func(split_eq.left_terms, split_eq.right_terms)
                    merged_nodes, merged_edges = merge_graphs(eq_nodes, eq_edges, split_eq_odes, split_eq_edges)
                    if visualize == True:
                        draw_graph(nodes=merged_nodes, edges=merged_edges, filename=split_file)

                    graph_dict = graph_to_gnn_format(merged_nodes, merged_edges, label=split_label,satisfiability=split_satisfiability)
                    # Dumping the dictionary to a JSON file
                    json_file = graph_folder+"/"+(strip_file_name_suffix(split_file) + ".graph.json").replace("train/","")
                    dump_to_json_with_format(graph_dict, json_file)




def output_eq_graphs(zip_file:str,graph_folder: str, graph_func: Callable, visualize: bool = False):
    parser = get_parser()
    with zipfile.ZipFile(zip_file, 'r') as zip_file_content:
        for f in zip_file_content.namelist():
            if fnmatch.fnmatch(f, '*.eq'):
    #eq_file_list = glob.glob(graph_folder + "/*.eq")
    #for file_path in eq_file_list:

                parsed_content = parser.parse(f,zip_file_content)
                # print("parsed_content:", parsed_content)

                answer_file = strip_file_name_suffix(f) + ".answer"
                with zip_file_content.open(answer_file) as file:
                #with open(answer_file, 'r') as file:
                    answer = file.read()
                    answer = answer.decode('utf-8')

                for eq in parsed_content["equation_list"]:
                    if visualize == True:
                        # visualize
                        pass # todo adapt to zip file
                        #eq.visualize_graph(file_path, graph_func)
                    # get gnn format
                    nodes, edges = graph_func(eq.left_terms, eq.right_terms)
                    satisfiability = answer
                    graph_dict = graph_to_gnn_format(nodes, edges, label=satisfiability_to_int_label[satisfiability],satisfiability=satisfiability)
                    # print(graph_dict)
                    # Dumping the dictionary to a JSON file
                    json_file = graph_folder+"/"+(strip_file_name_suffix(f) + ".graph.json").replace("train/","")
                    dump_to_json_with_format(graph_dict, json_file)



def get_parser():
    parser_type = EqParser()
    return Parser(parser_type)