import os
import sys
import configparser

# Read path from config.ini
config = configparser.ConfigParser()
config.read("config.ini")
path = config.get('Path','local')
sys.path.append(path)

from src.solver.Parser import Parser, EqParser, EqReader
from src.solver.Solver import Solver
from src.solver.utils import print_results,graph_func_map
from src.solver.algorithms import EnumerateAssignments, EnumerateAssignmentsUsingGenerator, \
    ElimilateVariablesRecursive, SplitEquations
import argparse


def main(args):
    algorithm_map = {"ElimilateVariablesRecursive": ElimilateVariablesRecursive,
                     "SplitEquations": SplitEquations}

    #parse argument
    arg_parser = argparse.ArgumentParser(description='Process command line arguments.')

    arg_parser.add_argument('file_path', type=str, help='Path to the file')
    arg_parser.add_argument('branch_method', type=str, #choices=['gnn', 'random', 'fixed'],
                        help='Branching method to be used')
    arg_parser.add_argument('--graph_type', type=str, default=None,
                        help='Type of graph (optional)')
    arg_parser.add_argument('--gnn_model_path', type=str,  default=None,
                            help='path to .pth file')
    arg_parser.add_argument('--gnn_task', type=str, default=None,
                            help='task_1, task_2,...')
    arg_parser.add_argument('--termination_condition', type=str, default="termination_condition_0",
                            help='termination_condition_0,termination_condition_1,termination_condition_2,...')
    arg_parser.add_argument('--order_equations_method', type=str, default="fixed",
                            help='fixed,random...')
    arg_parser.add_argument('--algorithm', type=str, default="ElimilateVariablesRecursive",
                            help='ElimilateVariablesRecursive,SplitEquations...')


    args = arg_parser.parse_args()

    # Accessing the arguments
    file_path = args.file_path
    branch_method = args.branch_method
    graph_type = args.graph_type
    gnn_model_path = args.gnn_model_path
    task=args.gnn_task
    termination_condition=args.termination_condition
    algorithm=algorithm_map[args.algorithm]
    order_equations_method=args.order_equations_method

    print(file_path, branch_method, graph_type)


    #parse file
    parser_type = EqParser()
    parser = Parser(parser_type)
    parsed_content = parser.parse(file_path)
    print("parsed_content:", parsed_content)

    algorithm_parameters = {"branch_method":branch_method,"graph_type":graph_type,"task":task,
                            "graph_func":graph_func_map[graph_type],"gnn_model_path":gnn_model_path,
                            "termination_condition":termination_condition,
                            "order_equations_method":order_equations_method} # branch_method [gnn,random,fixed]


    solver = Solver(algorithm=algorithm,algorithm_parameters=algorithm_parameters)

    result_dict = solver.solve(parsed_content, visualize=False,output_train_data=False)

    print_results(result_dict)


if __name__ == '__main__':
    main(sys.argv[1:])
