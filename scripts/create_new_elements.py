import pandas as pd
import os
import csv

def delete_data_except_first_row(file_path):
    # Construct the full path to the CSV file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "..", "run", file_path)

    # Read the data from the CSV file with 'utf-8' encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Retain the first row
    first_row = data[0]

    # Write only the first row back to the CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(first_row)

def copy_id_and_pos_columns(source_file_path, destination_file_path):
    # Construct the full paths to the CSV files
    current_directory = os.path.dirname(os.path.abspath(__file__))
    source_file_path = os.path.join(current_directory, "..", "data", source_file_path)
    destination_file_path = os.path.join(current_directory, "..", "run", destination_file_path)

    # Read the "ID" and "Pos" columns from the source file (gaffr.csv)
    source_df = pd.read_csv(source_file_path)
    id_column_data = source_df["ID"][0:]  # Excluding the header row (row 1)
    pos_column_data = source_df["Pos"][0:]  # Excluding the header row (row 1)
    cost_column_data = source_df["BV"][0:]  # Excluding the header row (row 1)
    name_column_data = source_df["Name"][0:]  # Excluding the header row (row 1)
    team_column_data = source_df["Team"][0:]  # Excluding the header row (row 1)

    # Read the "id" and "name" columns from the teams.csv file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    teams_file_path = os.path.join(current_directory, "../run/teams.csv")
    teams_df = pd.read_csv(teams_file_path)

    # Create a mapping between team names and their corresponding IDs
    team_id_mapping = dict(zip(teams_df["name"], teams_df["id"]))

    # Update the "team" column in the destination file (elements.csv) with the relevant IDs
    destination_df = pd.read_csv(destination_file_path)
    destination_df["team"] = team_column_data.map(team_id_mapping)

    # Update the "ID" and "team" columns in the destination file (elements.csv)
    destination_df["id"] = id_column_data
    destination_df["element_type"] = pos_column_data
    destination_df["now_cost"] = cost_column_data
    # Update the "now_cost" column in the destination file (elements.csv)
    destination_df["now_cost"] = destination_df["now_cost"] * 10
    destination_df["web_name"] = name_column_data

    # Amend the data in the "team" column based on the mapping provided
    team_mapping = {'G': 1, 'D': 2, 'M': 3, 'F': 4}
    destination_df["element_type"] = destination_df["element_type"].map(team_mapping)

    # Set every value in the "selected_by_percent" column to 0
    destination_df["selected_by_percent"] = 0

    # Write the updated "elements.csv" back to the file
    destination_df.to_csv(destination_file_path, index=False)

if __name__ == "__main__":
    file_name = "elements.csv"
    delete_data_except_first_row(file_name)

    source_file_name = "gaffr.csv"
    destination_file_name = "elements.csv"
    copy_id_and_pos_columns(source_file_name, destination_file_name)