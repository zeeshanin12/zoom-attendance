import pandas as pd
import os
from re import search
import argparse, sys

#python main.py --saved_chat_directory /Users/khanz/aisha-attendance/ --output_file_name out.csv

def is_present (input) :
    if search("present", input) :
        return True
    else :
        return False

def post_process(joined_df) :
    joined_df = joined_df.fillna(0).astype(int)
    joined_df.index = joined_df.index.str.title()
    joined_df.sort_index(inplace = True)
    return joined_df

def join_files(INPUT_FILE_PATH, student_names):
    # Read input saved chat file.
    df = pd.read_csv (INPUT_FILE_PATH, header = None)
    # Do some pre-processing.
    df.columns = ['line']
    lines = df["line"].str.split("\t From ").str[1]
    l = lines.apply(lambda e : e.split(' : '))
    df['name'] =  l.str[0].apply(lambda e : e[1:].lower())
    df['message'] =  l.str[1].apply(lambda e : e.lower())

    present_rows = df[df['message'].apply(lambda e : is_present(e))].copy()

    present_rows["is_present"]  = present_rows["message"].apply(lambda e : 1)
    present_rows.drop_duplicates(inplace = True)
    present_rows = present_rows[["name", "is_present"]].set_index('name')

    # Read class names file
    class_names = pd.read_csv (student_names, header = None)

    # Do some pre-processing on the dataframe.
    class_names.columns = ['name']
    class_names["name"] = class_names["name"].apply(lambda e : e.lower())
    class_names = class_names.set_index('name')

    # Join the 2 dataframes.
    joined_df = post_process(class_names.join(present_rows, how="outer", on="name"))
    left_joined_df = post_process(class_names.join(present_rows, how="left", on="name"))
    # Do some post processing
    matches = left_joined_df["is_present"].sum()

    return (matches, joined_df)

def get_max_join(filepath):
    student_list = [
            "./student_list/class_10a.csv",
            "./student_list/class_10b.csv",
            "./student_list/class_10c.csv",
            "./student_list/class_10d.csv",
            ]
    matches_list = []
    joined_df_list = []
    for student_names in student_list :
        matches, joined_df = join_files(filepath, student_names)
        matches_list.append(matches)
        joined_df_list.append(joined_df)

    max_joins_df = joined_df_list[matches_list.index(min(matches_list))]
    return(max_joins_df)


parser = argparse.ArgumentParser()

parser.add_argument('--saved_chat_directory', help = 'Directory to scan "meeting_saved_chat" files')
parser.add_argument('--output_file_name', help = 'File name of the output processed file')

args = parser.parse_args()

SAVED_CHAT_DIR = args.saved_chat_directory

for subdir, dirs, files in os.walk(SAVED_CHAT_DIR):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filepath.endswith("meeting_saved_chat"):
            print ("Processing file : " + filepath)
            df = get_max_join(filepath)

            output_file_name = filepath.replace("meeting_saved_chat", "attendance.csv")
            print ("Writing output to file : " + output_file_name)
            # Write the result to out tables.
            df.to_csv(output_file_name, index = True)
