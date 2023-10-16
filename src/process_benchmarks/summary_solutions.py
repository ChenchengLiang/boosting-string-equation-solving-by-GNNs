import csv
import os


def main():
    summary_folder = "/home/cheli243/Desktop/CodeToGit/string-equation-solver/boosting-string-equation-solving-by-GNNs/src/process_benchmarks/summary"


    for track in ["track_01","track_02","track_03"]:
        summary_file_dict={"this":"this_"+track+"_summary.csv",
                           "woorpje":"woorpje_"+track+"_summary.csv",
                           "z3":"z3_"+track+"_summary.csv",
                           "ostrich":"ostrich_"+track+"_summary.csv",
                           "cvc5":"cvc5_"+track+"_summary.csv"}

        summary_one_track(summary_folder,summary_file_dict,track)





def summary_one_track(summary_folder,summary_file_dict,track_name):
    first_summary_solver_row = ["file_names"]
    first_summary_title_row = [""]
    first_summary_data_rows = []

    second_summary_title_row = ["solver"]
    second_summary_data_rows = []

    for solver, summary_file in summary_file_dict.items():
        first_summary_solver_row.extend([solver, solver])

        reconstructed_list_title, reconstructed_list, reconstructed_summary_title, reconstructed_summary_data = extract_one_csv_data(summary_folder,
            summary_file)
        first_summary_title_row.extend(reconstructed_list_title[1:])
        if len(first_summary_data_rows) == 0:
            first_summary_data_rows = [[] for x in reconstructed_list]


        # print("solver",solver)
        # print(reconstructed_list)
        for f, r in zip(first_summary_data_rows, reconstructed_list):
            if len(f)==0:
                f.extend(r)
            else:
                file_name_1 = f[0].replace(".eq", "").replace(".smt2", "").replace(".smt", "")
                for rr in reconstructed_list:
                    rr=[x for x in rr if x!=""]
                    file_name_2 = rr[0].replace(".eq","").replace(".smt2","").replace(".smt","")
                    if file_name_1 == file_name_2:
                        f.extend(rr[1:])



        if len(second_summary_title_row) == 1:
            second_summary_title_row.extend(reconstructed_summary_title)

        second_summary_data_rows.append([solver] + reconstructed_summary_data)

    summary_path = os.path.join(summary_folder, track_name+"_reconstructed_summary_1.csv")
    if os.path.exists(summary_path):
        os.remove(summary_path)

    # Writing to csv file
    with open(summary_path, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Writing the column solvers
        csvwriter.writerow(first_summary_solver_row)
        # Writing the column headers
        csvwriter.writerow(first_summary_title_row)

        for row in first_summary_data_rows:
            csvwriter.writerow(row)

    summary_path = os.path.join(summary_folder, track_name+"_reconstructed_summary_2.csv")
    if os.path.exists(summary_path):
        os.remove(summary_path)

    # Writing to csv file
    with open(summary_path, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(second_summary_title_row)
        csvwriter.writerows(second_summary_data_rows)


def extract_one_csv_data(summary_folder,summary_file):

    summary_path = os.path.join(summary_folder, summary_file)
    with open(summary_path, 'r') as file:
        reader = csv.reader(file)
        reader = list(reader)
        reconstructed_first_row = reader[1][:3]
        reconstructed_list = [reconstructed_first_row] + reader[2:]
        reconstructed_list_title = reader[0][:3]
        reconstructed_summary_title = reader[0][4:]
        reconstructed_summary_data = reader[1][4:]



        # print(reconstructed_list_title)
        # for row in reconstructed_list:
        #     print(row)  # Each row is a list of strings

        # print(reconstructed_summary_title)
        # print(reconstructed_summary_data)

        return reconstructed_list_title,reconstructed_list,reconstructed_summary_title,reconstructed_summary_data



if __name__ == '__main__':
    main()