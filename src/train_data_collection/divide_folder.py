import sys
import configparser

# Read path from config.ini
config = configparser.ConfigParser()
config.read("config.ini")
path = config.get('Path', 'local')
sys.path.append(path)

import os
from src.solver.Constants import project_folder, bench_folder

from src.train_data_collection.utils import dvivde_track_for_cluster
from src.solver.independent_utils import get_folders
import shutil

def main():
    # generate track
    track_name="01_track_multi_word_equations_generated_train_1_20000_eq_number_20_UNSAT_train"
    file_folder="UNSAT"
    track_folder = bench_folder + "/"+track_name
    print(track_folder)

    # divide tracks
    dvivde_track_for_cluster(track_folder,file_folder=file_folder, chunk_size=50)

    divided_folder_list = [train_folder for train_folder in get_folders(f"{track_folder}/{file_folder}") if
                           "divided" in train_folder]
    print("divided_folder_list",len(divided_folder_list))

    for divided_folder in divided_folder_list:
        temp_file=f"{track_folder}/{file_folder}/temp"
        shutil.move(f"{track_folder}/{file_folder}/{divided_folder}",temp_file)
        os.mkdir(f"{track_folder}/{file_folder}/{divided_folder}")
        shutil.move(temp_file,f"{track_folder}/{file_folder}/{divided_folder}/{file_folder}")


if __name__ == '__main__':
    main()
