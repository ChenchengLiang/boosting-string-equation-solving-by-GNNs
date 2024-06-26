import configparser
import os
import sys

# Read path from config.ini
config = configparser.ConfigParser()
config.read("config.ini")
path = config.get('Path', 'local')

sys.path.append(path)
from src.solver.Constants import bench_folder, project_folder
from src.solver.independent_utils import write_configurations_to_json_file


def main():
    model_folder = project_folder + "/" + "Models/"
    task = "task_3"
    graph_type = "graph_5"
    model_type = "GCNSplit"  # "GINSplit"
    benchmark_name = "01_track_eval_task_3_1_1000"
    solver_param_list = [
        # ["this", ["random", f"--termination_condition termination_condition_0"]],
        # ["this", ["random", f"--termination_condition termination_condition_1"]],
        # ["this", ["random", f"--termination_condition termination_condition_2"]],
        # ["this", ["fixed", f"--termination_condition termination_condition_0"]],
        # ["this", ["fixed", f"--termination_condition termination_condition_1"]],
        # ["this", ["fixed", f"--termination_condition termination_condition_2"]],

        # ["this", ["gnn", "--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_GCN.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this", ["gnn:random", "--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_GCN.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this", ["gnn:fixed", "--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_GCN.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this",["gnn", "--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_GIN.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this", ["gnn:random", "--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_GIN.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this",["gnn:fixed","--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_GIN.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this", ["gnn","--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_GCNwithGAP.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this",["gnn:random", "--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_GCNwithGAP.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this",["gnn:fixed", "--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_GCNwithGAP.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this", ["gnn", "--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_MultiGNNs.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this",["gnn:random","--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_MultiGNNs.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],
        # ["this",["gnn:fixed", "--graph_type graph_2", "--gnn_model_path " + model_folder + "model_0_graph_2_MultiGNNs.pth", f"--gnn_task {task}",f"--termination_condition {termination_condition}"]],

        # when read the model model_0_graph_2_GCNSplit.pth, it points to two files model_2_graph_2_GCNSplit.pth and model_3_graph_2_GCNSplit.pth
        ["this", ["gnn", f"--termination_condition termination_condition_0", f"--graph_type {graph_type}",
                  "--gnn_model_path " + model_folder + f"model_0_{graph_type}_{model_type}.pth",
                  f"--gnn_task {task}"]],
        ["this", ["gnn", f"--termination_condition termination_condition_1", f"--graph_type {graph_type}",
                  "--gnn_model_path " + model_folder + f"model_0_{graph_type}_{model_type}.pth",
                  f"--gnn_task {task}"]],
        ["this", ["gnn", f"--termination_condition termination_condition_2", f"--graph_type {graph_type}",
                  "--gnn_model_path " + model_folder + f"model_0_{graph_type}_{model_type}.pth",
                  f"--gnn_task {task}"]],

        ["this",
         ["gnn:random", f"--termination_condition termination_condition_0", f"--graph_type {graph_type}", "--gnn_model_path " + model_folder + f"model_0_{graph_type}_{model_type}.pth",
          f"--gnn_task {task}"]],
        ["this",
         ["gnn:random", f"--termination_condition termination_condition_1", f"--graph_type {graph_type}", "--gnn_model_path " + model_folder + f"model_0_{graph_type}_{model_type}.pth",
          f"--gnn_task {task}"]],
        ["this",
         ["gnn:random", f"--termination_condition termination_condition_2", f"--graph_type {graph_type}", "--gnn_model_path " + model_folder + f"model_0_{graph_type}_{model_type}.pth",
          f"--gnn_task {task}"]],

        ["this",
         ["gnn:fixed", f"--termination_condition termination_condition_0", f"--graph_type {graph_type}", "--gnn_model_path " + model_folder + f"model_0_{graph_type}_{model_type}.pth",
          f"--gnn_task {task}"]],
        ["this",
         ["gnn:fixed", f"--termination_condition termination_condition_1", f"--graph_type {graph_type}", "--gnn_model_path " + model_folder + f"model_0_{graph_type}_{model_type}.pth",
          f"--gnn_task {task}"]],
        ["this",
         ["gnn:fixed", f"--termination_condition termination_condition_2", f"--graph_type {graph_type}", "--gnn_model_path " + model_folder + f"model_0_{graph_type}_{model_type}.pth",
          f"--gnn_task {task}"]],

        # ["z3", []],
        # ["z3-noodler", ["smt.string_solver=\"noodler\""]],
        # ["woorpje", []],
        # ["ostrich", []],
        # ["cvc5", []],
    ]

    benchmark_dict = {
        # "test_track": bench_folder + "/test",
        # "example_track": bench_folder + "/examples",
        # "track_01": bench_folder + "/01_track",
        # "g_track_01_sat":bench_folder + "/01_track_generated/SAT",
        # "g_track_01_mixed": bench_folder + "/01_track_generated/mixed",
        # "g_track_01_eval":bench_folder + "/01_track_generated_eval_data",
        # "track_02": bench_folder + "/02_track",
        # "track_03": bench_folder + "/03_track",
        # "track_04": bench_folder + "/04_track",
        # "track_05": bench_folder + "/05_track",
        # "track_random_train": bench_folder + "/random_track_train",
        # "track_random_eval": bench_folder + "/random_track_eval",
        # "track_01_generated_SAT_train": bench_folder + "/01_track_generated_SAT_train/ALL",
        # "track_01_generated_SAT_eval": bench_folder + "/01_track_generated_SAT_eval",
    }


    benchmark_folder = benchmark_name + "/ALL"
    folder_number = sum(
        [1 for fo in os.listdir(bench_folder + "/" + benchmark_folder) if "divided" in os.path.basename(fo)])
    for i in range(folder_number):
        divided_folder_index = i + 1
        benchmark_dict[benchmark_name + "_divided_" + str(
            divided_folder_index)] = bench_folder + "/" + benchmark_folder + "/divided_" + str(divided_folder_index)

    configuration_list = []
    for solver_param in solver_param_list:
        solver = solver_param[0]
        parameters_list = solver_param[1]

        for benchmark_name, benchmark_folder in benchmark_dict.items():
            configuration_list.append(
                {"solver": solver, "parameters_list": parameters_list, "benchmark_name": benchmark_name,
                 "benchmark_folder": benchmark_folder, "summary_folder_name": benchmark_name + "_summary"})

    # Writing the dictionary to a JSON file
    configuration_folder = project_folder + "/src/process_benchmarks/configurations"
    write_configurations_to_json_file(configuration_folder=configuration_folder, configurations=configuration_list)

    print("done")


if __name__ == '__main__':
    main()
