import os
import shutil
import sys
import configparser

from src.solver.algorithms.split_equations_extract_data import SplitEquationsExtractData

# Read path from config.ini
config = configparser.ConfigParser()
config.read("config.ini")
path = config.get('Path', 'local')
sys.path.append(path)

import glob
import sys
from src.solver.Constants import project_folder

sys.path.append(project_folder)
from src.solver.Parser import Parser, EqParser, EqReader
from src.solver.Solver import Solver
from src.solver.utils import print_results, graph_func_map
from src.solver.algorithms import EnumerateAssignments, EnumerateAssignmentsUsingGenerator, ElimilateVariablesRecursive, \
    SplitEquations
from src.solver.Constants import algorithm_timeout
from src.solver.DataTypes import Equation
from src.solver.Constants import project_folder, bench_folder, UNKNOWN, SAT, UNSAT, recursion_limit
from src.solver.independent_utils import strip_file_name_suffix, zip_folder, get_folders
from src.process_benchmarks.utils import run_on_one_problem


def main():
    benchmark = "choose_eq_train"

    # algorithm = ElimilateVariablesRecursive
    # algorithm_parameters = {"branch_method": "extract_branching_data_task_3", "extract_algorithm": "fixed",
    #                         "termination_condition": "termination_condition_0"}  # extract_branching_data_task_2

    algorithm = SplitEquationsExtractData
    algorithm_parameters={"branch_method": "fixed", "order_equations_method": "category",
                                           "termination_condition": "termination_condition_3","task":"dynamic_embedding"}

    sys.setrecursionlimit(recursion_limit)
    benchmark_path = bench_folder + "/" + benchmark
    folder_list = [folder for folder in get_folders(benchmark_path) if
                   "divided" in folder or "valid" in folder]
    print(folder_list)
    if len(folder_list) != 0:
        for folder in folder_list:
            generate_train_data_in_one_folder(benchmark_path + "/" + folder, algorithm, algorithm_parameters)
    else:
        generate_train_data_in_one_folder(benchmark_path, algorithm, algorithm_parameters)


def generate_train_data_in_one_folder(folder, algorithm, algorithm_parameters):
    # prepare train folder
    all_eq_folder = folder+ "/SAT"
    train_eq_folder = folder+ "/train"

    # copy answers from divide folder
    # divided_folder = benchmark + "/ALL"
    # folder_number = sum(
    #     [1 for fo in os.listdir(bench_folder + "/" + divided_folder) if "divided" in os.path.basename(fo)])
    # for i in range(folder_number):
    #     divided_folder_index = i + 17
    #     for answer_file in glob.glob(
    #             bench_folder + "/" + divided_folder + "/divided_" + str(divided_folder_index) + "/*.answer"):
    #         shutil.copy(answer_file, all_eq_folder)

    if not os.path.exists(train_eq_folder):
        os.mkdir(train_eq_folder)
    else:
        shutil.rmtree(train_eq_folder)
        os.mkdir(train_eq_folder)
    for f in glob.glob(all_eq_folder + "/*.eq") + glob.glob(all_eq_folder + "/*.answer"):
        shutil.copy(f, train_eq_folder)

    # extract train data
    eq_file_list = glob.glob(train_eq_folder + "/*.eq")
    eq_file_list_len = len(eq_file_list)
    for i, file_path in enumerate(eq_file_list):
        file_name = strip_file_name_suffix(file_path)
        print(f"-- {i}/{eq_file_list_len} --")
        print(file_path)

        # get satisfiability
        answer_file_path = file_name + ".answer"
        if os.path.exists(answer_file_path):  # read file answer
            print("read answer from file")
            with open(answer_file_path, "r") as f:
                satisfiability = f.read().strip("\n")
        else:
            result_dict = run_on_one_problem(file_path=file_path,
                                             parameters_list=["fixed",
                                                              f"--termination_condition termination_condition_0"],
                                             solver="this", solver_log=False)
            satisfiability = result_dict["result"]

        print("satisfiability:", satisfiability)

        if satisfiability == SAT or satisfiability == UNSAT:
            parser_type = EqParser()
            parser = Parser(parser_type)
            parsed_content = parser.parse(file_path)
            # print("parsed_content:", parsed_content)

            solver = Solver(algorithm=algorithm, algorithm_parameters=algorithm_parameters)

            result_dict = solver.solve(parsed_content, visualize=False, output_train_data=True)

            # print_results(result_dict)

    # compress
    zip_folder(folder_path=train_eq_folder, output_zip_file=train_eq_folder + ".zip")
    shutil.rmtree(train_eq_folder)
    print("done")


if __name__ == '__main__':
    main()
