import configparser
import glob
import os
import sys

# Read path from config.ini
config = configparser.ConfigParser()
config.read("config.ini")
path = config.get('Path','local')
sys.path.append(path)

from src.solver.Constants import bench_folder,project_folder, UNKNOWN,SUCCESS,FAIL,RED,COLORRESET
from src.solver.Parser import Parser, EqParser,SMT2Parser
from src.solver.Solver import Solver
from src.solver.utils import print_results,graph_func_map
from src.solver.algorithms import ElimilateVariablesRecursive
from src.solver.independent_utils import strip_file_name_suffix,check_list_consistence
from src.process_benchmarks.utils import run_on_one_problem
from src.process_benchmarks.eq2smt_utils import one_eq_file_to_smt2



def main():
    configuration_list=[
        {"task":"task_1","graph_type":"graph_1","branch_method":"fixed"}
    ]

    # test
    result_list=[]
    for config_dict in configuration_list:
        for file_path in glob.glob(bench_folder+"/regression_test/*.eq"):
            result_str=test_one_file(file_path,config_dict)
            result_list.append(result_str)

    # print results
    print("-"*10,"result list","-"*10)
    for r in result_list:
        print(r)


def test_one_file(file_path,config_dict):
    parser_type = EqParser() if file_path.endswith(".eq") else SMT2Parser()
    parser = Parser(parser_type)
    parsed_content = parser.parse(file_path)
    print("parsed_content:", parsed_content)

    graph_type = config_dict["graph_type"]
    task = config_dict["task"]
    gnn_model_path = project_folder + "/Models/model_0_" + graph_type + "_GCNSplit.pth"

    algorithm_parameters = {"branch_method": config_dict["branch_method"], "task": task, "graph_type": graph_type,
                            "graph_func": graph_func_map[graph_type],
                            "gnn_model_path": gnn_model_path,
                            "extract_algorithm": "fixed"}  # branch_method [extract_branching_data_task_2,random,fixed,gnn,gnn:fixed,gnn:random]

    # solver = Solver(algorithm=SplitEquations,algorithm_parameters=algorithm_parameters)
    solver = Solver(algorithm=ElimilateVariablesRecursive, algorithm_parameters=algorithm_parameters)
    # solver = Solver(algorithm=ElimilateVariables,algorithm_parameters=algorithm_parameters)
    # solver = Solver(EnumerateAssignmentsUsingGenerator, max_variable_length=max_variable_length,algorithm_parameters=algorithm_parameters)
    # solver = Solver(algorithm=EnumerateAssignments,max_variable_length=max_variable_length,algorithm_parameters=algorithm_parameters)
    result_dict = solver.solve(parsed_content, visualize=True, output_train_data=False)
    print_results(result_dict)


    print("-"*10,"check consistence between solvers","-"*10)
    for sh_file in glob.glob(bench_folder+"/src/process_benchmarks/temp_shell/*"):
        os.remove(sh_file)
    if not os.path.exists(strip_file_name_suffix(file_path)+".smt2"):
        one_eq_file_to_smt2(file_path)


    satisfiability_list=[]
    if result_dict["result"] != UNKNOWN:
        satisfiability_list.append(result_dict["result"])


    for solver in ["z3","cvc5","ostrich","woorpje"]:
        if solver == "woorpje":
            file = strip_file_name_suffix(file_path)+".eq"
        else:
            file = strip_file_name_suffix(file_path)+".smt2"
        other_solver_result_dict = run_on_one_problem(file_path=file, parameters_list=[], solver=solver, solver_log=False)
        if other_solver_result_dict["result"] != UNKNOWN:
            satisfiability_list.append(other_solver_result_dict["result"])

    if len(satisfiability_list)==0:
        print("consistance", UNKNOWN)
        consistance=True
    else:
        consistance=check_list_consistence(satisfiability_list)
        if consistance==True:
            print("consistance")
        else:
            print(RED,"inconsistance",COLORRESET)

    print("-" * 10, "check consistence between solvers done", "-" * 10)

    print("-" * 10, "check .answer file", "-" * 10)
    # read answer file
    answer_file = strip_file_name_suffix(file_path) + ".answer"
    if os.path.exists(answer_file):
        with open(answer_file) as f:
            answer = f.read()
    else:
        answer=UNKNOWN

    satisfiability=result_dict["result"]
    if satisfiability == answer:
        return f"{SUCCESS}, satisfiability: {satisfiability}, answer: {answer}, consistence: {consistance}, {os.path.basename(file_path)}"
    else:
        return f"{FAIL}, satisfiability: {satisfiability}, answer: {answer}, consistence: {consistance}, {os.path.basename(file_path)}"

 

if __name__ == '__main__':
    main()