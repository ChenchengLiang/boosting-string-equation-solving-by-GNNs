import os
import sys
import configparser

# Read path from config.ini
config = configparser.ConfigParser()
config.read("config.ini")
path = config.get('Path','local')
sys.path.append(path)

from src.solver.Constants import bench_folder,project_folder,UNKNOWN
from src.solver.Parser import Parser, EqParser,SMT2Parser
from src.solver.Solver import Solver
from src.solver.utils import print_results,graph_func_map
from src.solver.algorithms import EnumerateAssignments,EnumerateAssignmentsUsingGenerator,ElimilateVariables,ElimilateVariablesRecursive,SplitEquations
from src.solver.DataTypes import Equation
from src.solver.independent_utils import strip_file_name_suffix
def main():
    #debug
    #file_path=bench_folder +"/examples/03_track_52.eq"
    # example path
    #file_path=bench_folder +"/regression_test/g_03_track_27.eq"
    file_path=bench_folder +"/temp/output.eq"

    #file_path = bench_folder + "/examples/2_task_2/ALL/ALL/01_track_2.eq"
    #file_path= bench_folder +"/examples/01_track_4.eq"
    #file_path = bench_folder+"/examples/43/01_track_43.eq"
    #file_path = bench_folder+"/examples/g_01_track_85.eq"
    #file_path = bench_folder + "/examples/32/g_01_track_32.eq"
    #file_path = bench_folder + "/examples/g_01_SAT/g_01_track_SAT_1.eq"
    #file_path = bench_folder + "/examples/g_02_SAT/g_01_track_SAT_2.eq"
    #file_path = bench_folder + "/examples/g_01_SAT_464/g_01_track_SAT_464.eq"
    #file_path = bench_folder + "/examples/g_random_track_1144.eq"

    #file_path = bench_folder +"/test/03_track_11.eq"
    # Woorpje_benchmarks path
    #SAT
    #file_path = bench_folder +"/01_track/01_track_1.eq"
    #file_path = bench_folder +"/01_track/01_track_2.eq"
    #file_path = bench_folder +"/01_track/01_track_3.eq"
    #file_path = bench_folder +"/01_track/01_track_4.eq"
    #file_path = bench_folder +"/01_track/01_track_5.eq"
    #file_path = bench_folder +"/01_track/01_track_36.eq"
    #file_path = bench_folder +"/01_track/01_track_37.eq"
    #file_path = bench_folder +"/01_track/01_track_58.eq"
    #file_path = bench_folder +"/01_track/01_track_93.eq"
    #file_path = bench_folder +"/01_track/01_track_192.eq"

    #UNSAT
    #file_path = bench_folder +"/03_track/03_track_14.eq"
    #file_path = bench_folder +"/03_track/03_track_7.eq"
    #file_path = bench_folder +"/03_track/03_track_11.eq"
    #file_path = bench_folder +"/03_track/03_track_17.eq"

    #multiple equations
    #file_path = bench_folder + "/examples/multi_eqs/1/test1.eq" #SAT
    #file_path=bench_folder +"/examples/multi_eqs/2/test2.eq" #UNSAT
    #file_path = bench_folder + "/examples/multi_eqs/4/g_04_track_generated_train_1_1000_4.eq"  # UNSAT
    #file_path = bench_folder + "/examples/multi_eqs/5/g_04_track_generated_train_1_1000_5.eq"  # UNSAT
    #file_path = bench_folder + "/examples/multi_eqs/26/04_track_26.eq"  # SAT
    #file_path=bench_folder +"/examples/multi_eqs/test3.eq" #UNSAT
    #file_path=bench_folder +"/examples/multi_eqs/04_track_6.eq" #SAT
    #file_path=bench_folder +"/examples/multi_eqs/04_track_59.eq" #UNSAT
    #file_path=bench_folder +"/examples/multi_eqs/04_track_172.eq" #SAT
    #file_path = bench_folder + "/examples/multi_eqs/04_track_189.eq"  # SAT
    #file_path = bench_folder + "/examples/multi_eqs/04_track_19.eq"  # UNSAT
    #file_path = bench_folder + "/examples/multi_eqs/04_track_80.eq"  # UNSAT
    #file_path = bench_folder + "/examples/multi_eqs/04_track_180.eq"  # UNSAT
    #file_path = bench_folder + "/examples/multi_eqs/04_track_183.eq"  # UNSAT

    #smt format
    #file_path=bench_folder +"/example_smt/1586.corecstrs.readable.smt2"


    parser_type = EqParser() if file_path.endswith(".eq") else SMT2Parser()
    parser = Parser(parser_type)
    parsed_content = parser.parse(file_path)
    print("parsed_content:", parsed_content)

    graph_type="graph_1"
    task="task_3"
    gnn_model_path=project_folder+"/Models/model_0_"+graph_type+"_GCNSplit.pth"

    algorithm_parameters = {"branch_method":"fixed","task":task,"graph_type":graph_type,"graph_func":graph_func_map[graph_type],
                            "gnn_model_path":gnn_model_path,"extract_algorithm":"fixed",
                            "termination_condition":"execute_termination_condition_0"} # branch_method [extract_branching_data_task_2,random,fixed,gnn,gnn:fixed,gnn:random]

    #solver = Solver(algorithm=SplitEquations,algorithm_parameters=algorithm_parameters)
    solver = Solver(algorithm=ElimilateVariablesRecursive,algorithm_parameters=algorithm_parameters)
    #solver = Solver(algorithm=ElimilateVariables,algorithm_parameters=algorithm_parameters)
    #solver = Solver(EnumerateAssignmentsUsingGenerator, max_variable_length=max_variable_length,algorithm_parameters=algorithm_parameters)
    #solver = Solver(algorithm=EnumerateAssignments,max_variable_length=max_variable_length,algorithm_parameters=algorithm_parameters)
    result_dict = solver.solve(parsed_content,visualize=True,output_train_data=False)

    print_results(result_dict)


if __name__ == '__main__':
    main()
