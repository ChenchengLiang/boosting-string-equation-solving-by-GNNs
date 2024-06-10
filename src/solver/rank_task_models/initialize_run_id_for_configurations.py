import configparser
import os
import sys

# Read path from config.ini
config = configparser.ConfigParser()
config.read("config.ini")
path = config.get('Path','local')
sys.path.append(path)

os.environ["DGLBACKEND"] = "pytorch"
import dgl
import dgl.data
import torch
from typing import Dict, List, Any
from src.solver.Constants import project_folder
import mlflow
import argparse
import json
import datetime
import subprocess
from src.solver.independent_utils import color_print,get_folders
import signal
import torch.nn as nn
from src.solver.models.train_util import (initialize_model_structure, load_train_and_valid_dataset, training_phase,
                                          validation_phase,
                                          initialize_train_objects, log_and_save_best_model, save_checkpoint,
                                          update_config_file, data_loader_2, get_data_distribution,
                                          training_phase_without_loader, validation_phase_without_loader, data_loader_3,
                                          log_metrics_with_lock)

from src.solver.models.utils import device_info
from src.solver.rank_task_models.train_utils import initialize_model, read_dataset_from_zip
from torch.nn.parallel import DistributedDataParallel as DDP

import torch.distributed as dist
import torch.multiprocessing as mp
from torch.multiprocessing import SimpleQueue

def main():
    # parse argument
    arg_parser = argparse.ArgumentParser(description='Process command line arguments.')
    arg_parser.add_argument('--configuration_file', type=str, default=None,
                            help='path to configuration json file ')
    args = arg_parser.parse_args()
    # Accessing the arguments
    configuration_file = args.configuration_file
    if configuration_file is not None:
        # read json file
        with open(configuration_file) as f:
            train_config = json.load(f)
    else:
        print("No configuration file")



    train_config = initiate_run_id_for_a_configuration(train_config)


    update_config_file(configuration_file,train_config)


    print("done")


def initiate_run_id_for_a_configuration(train_config):
    device_info()
    train_config["device"] = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    benchmark_folder = config['Path']['woorpje_benchmarks']
    today = datetime.date.today().strftime("%Y-%m-%d")
    mlflow_ui_process = subprocess.Popen(['mlflow', 'ui'], preexec_fn=os.setpgrp)

    benchmark_folder_list=get_folders(benchmark_folder+"/"+train_config["benchmark"])
    train_folder_list=[folder for folder in benchmark_folder_list if "divided" in folder]
    experiment_name = today + "-" + train_config["benchmark"]
    if "divided_1" in train_folder_list:
        train_data_folder_epoch_map:Dict[str,int]={folder: 0 for folder in train_folder_list}
    else:
        train_data_folder_epoch_map:Dict[str,int]={train_config["benchmark"]: 0}
    train_config["train_data_folder_epoch_map"]=train_data_folder_epoch_map
    train_config["experiment_name"]=experiment_name

    mlflow.set_experiment(experiment_name)
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    torch.autograd.set_detect_anomaly(True)
    with mlflow.start_run() as mlflow_run:
        train_config["run_id"] = mlflow_run.info.run_id
        train_config["experiment_id"] = mlflow_run.info.experiment_id
        train_config["current_train_folder"] = train_config["benchmark"]+"/"+list(train_config["train_data_folder_epoch_map"].items())[0][0]
        mlflow.log_params(train_config)
        train_config=train_one_epoch_and_get_run_id(train_config)

    mlflow_ui_process.terminate()
    os.killpg(os.getpgid(mlflow_ui_process.pid), signal.SIGTERM)
    return train_config


def train_one_epoch_and_get_run_id(parameters):
    ############### Initialize training parameters ################
    model = initialize_model(parameters)
    parameters["model_save_path"] = os.path.join(project_folder, "Models",
                                                 f"model_{parameters['graph_type']}_{parameters['model_type']}.pth")

    parameters["benchmark_folder"]=parameters["benchmark"]
    train_dataset = read_dataset_from_zip(parameters,os.path.basename(parameters["current_train_folder"]) )
    valid_dataset = read_dataset_from_zip(parameters,"valid_data")
    dataset = {"train": train_dataset, "valid": valid_dataset}
    get_data_distribution(dataset, parameters)
    train_dataloader, valid_dataloader = data_loader_2(dataset, parameters)
    get_data_distribution(dataset, parameters)
    optimizer = torch.optim.Adam(model.parameters(), lr=parameters["learning_rate"])
    loss_function = nn.CrossEntropyLoss()
    best_model = None
    best_valid_loss = float('inf')  # Initialize with a high value
    best_valid_accuracy = float('-inf')  # Initialize with a low value
    epoch_info_log = ""
    check_point_model_path = parameters["run_id"] + f"_checkpoint_model_{parameters['label_size']}.pth"
    classification_type = "multi_classification"
    epoch=1
    index=1
    #
    # torch.multiprocessing.set_sharing_strategy('file_system')
    # world_size = torch.cuda.device_count()
    # queue = SimpleQueue()
    # mp.spawn(train_and_valid, args=(world_size, queue, parameters,model,best_model,best_valid_loss,
    #                                 best_valid_accuracy,dataset,loss_function,optimizer,
    #                                 classification_type,check_point_model_path,epoch_info_log,epoch,index),
    #          nprocs=world_size, join=True)
    # results = [queue.get() for _ in range(world_size)]
    # return results[-1]
    #


    parameters["device"]=f"cuda:{0}"
    model.to(parameters["device"])

    # Training Phase
    model, avg_train_loss = training_phase(model, train_dataloader, loss_function, optimizer, parameters)

    # Validation Phase
    model, avg_valid_loss, valid_accuracy = validation_phase(model, valid_dataloader, loss_function,
                                                             classification_type, parameters)

    # Save based on specified criterion
    best_model, best_valid_loss, best_valid_accuracy, epoch_info_log = log_and_save_best_model(parameters, epoch,
                                                                                               best_model, model,
                                                                                               "multi_class",
                                                                                               parameters[
                                                                                                   "label_size"],
                                                                                               avg_train_loss,
                                                                                               avg_valid_loss,
                                                                                               valid_accuracy,
                                                                                               best_valid_loss,
                                                                                               best_valid_accuracy,
                                                                                               epoch_info_log,
                                                                                               index)
    save_checkpoint(model, optimizer, epoch, best_valid_loss, best_valid_accuracy, parameters,
                    filename=check_point_model_path)

    # Return the trained model and the best metrics
    best_metrics = {f"best_valid_loss_multi_class_{parameters['label_size']}": best_valid_loss,
                    f"best_valid_accuracy_multi_class_{parameters['label_size']}": best_valid_accuracy}

    mlflow.log_metrics(best_metrics)

    parameters["train_data_folder_epoch_map"][os.path.basename(parameters["current_train_folder"])] = 1
    print("-" * 10, "train finished", "-" * 10)
    return parameters

def init_process(rank, world_size, backend='nccl'):
    dist.init_process_group(backend, rank=rank, world_size=world_size)

def train_and_valid(rank, world_size,queue,parameters,model,best_model,best_valid_loss,
                    best_valid_accuracy,dataset,loss_function,
                    optimizer,classification_type,check_point_model_path,epoch_info_log,epoch,index):
    # Initialize the process group
    init_process(rank, world_size)

    # Set the device
    torch.cuda.set_device(rank)
    device = torch.device(f'cuda:{rank}')
    model.to(device)

    # Wrap the model
    model = DDP(model, device_ids=[rank])

    train_dataloader, valid_dataloader = data_loader_3(dataset, parameters)


    # Training Phase
    model, avg_train_loss = training_phase(model, train_dataloader, loss_function, optimizer, parameters,device=device)

    # Validation Phase
    model, avg_valid_loss, valid_accuracy = validation_phase(model, valid_dataloader, loss_function,
                                                             classification_type, parameters,device=device)




    best_model, best_valid_loss, best_valid_accuracy, epoch_info_log = log_and_save_best_model(parameters, epoch,
                                                                                               best_model, model,
                                                                                               "multi_class",
                                                                                               parameters[
                                                                                                   "label_size"],
                                                                                               avg_train_loss,
                                                                                               avg_valid_loss,
                                                                                               valid_accuracy,
                                                                                               best_valid_loss,
                                                                                               best_valid_accuracy,
                                                                                               epoch_info_log,
                                                                                               index)
    save_checkpoint(model, optimizer, epoch, best_valid_loss, best_valid_accuracy, parameters,
                    filename=check_point_model_path)

    # Return the trained model and the best metrics
    best_metrics = {f"best_valid_loss_multi_class_{parameters['label_size']}": best_valid_loss,
                    f"best_valid_accuracy_multi_class_{parameters['label_size']}": best_valid_accuracy}

    #log_metrics_with_lock(best_metrics, lock_file=os.path.join(project_folder, "Models", "best_metrics_each_epoch.lock"))
    mlflow.log_metrics(best_metrics)

    parameters["train_data_folder_epoch_map"][os.path.basename(parameters["current_train_folder"])] = 1
    print("-" * 10, "train finished", "-" * 10)

    queue.put(parameters)

    dist.destroy_process_group()
    #return parameters


if __name__ == '__main__':
    main()