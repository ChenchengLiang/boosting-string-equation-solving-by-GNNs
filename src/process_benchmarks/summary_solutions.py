import os
import sys
import configparser

# Read path from config.ini
config = configparser.ConfigParser()
config.read("config.ini")
path = config.get('Path','local')
sys.path.append(path)

import csv
import glob
import os
from src.solver.independent_utils import strip_file_name_suffix
from src.process_benchmarks.utils import summary_one_track
from src.solver.Constants import project_folder,bench_folder
import argparse

def main():
    # parse argument
    arg_parser = argparse.ArgumentParser(description='Process command line arguments.')
    arg_parser.add_argument('--bench_name', type=str, default=None, help='bench name  ')

    args = arg_parser.parse_args()

    # Accessing the arguments
    bench_name = args.bench_name
    if bench_name is None:
        bench_name="03_track_train_task_3_5001_10000"


    summary_folder = project_folder+"/src/process_benchmarks/summary"


    for track in [bench_name]: #["track_01","track_02","track_03",g_track_01_mixed,track_random_eval,track_random_train,track_01_generated_SAT_eval]
        summary_file_dict={}
        for f in glob.glob(project_folder+"/src/process_benchmarks/summary/to_summary/*.csv"):
            if track in f:
                f=f[f.rfind("/")+1:]
                solver=f[:f.find("_")]
                parameter_str=f[f.find("_")+1:f.find(track)-1]
                #print(solver)
                #print(parameter_str)
                if solver == "this":
                    summary_file_dict[solver+":"+parameter_str]=solver+"_"+parameter_str+"_"+track+"_summary.csv"
                else:
                    summary_file_dict[
                        solver + ":" + parameter_str] = solver  + "_" + track + "_summary.csv"
        print(summary_file_dict)
        summary_one_track(summary_folder, summary_file_dict, track)







if __name__ == '__main__':
    main()