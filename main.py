import pandas as pd
import os
from re import search
import argparse, sys

#python main.py --saved_chat_directory /Users/khanz/aisha-attendance/ --output_file_name out.csv
# python main.py --saved_chat_directory ./zoom/
def is_present (input) :
    if search("present", str(input)) :
        return True
    else :
        return False

def join_files(SAVED_CHAT_PATH, STUDENT_NAMES_PATH):
    # Read input saved chat file.
    saved_chat_df= pd.read_csv(SAVED_CHAT_PATH, header = None, delimiter = '\n')
    # Do some pre-processing.
    saved_chat_df.columns = ['line']
    saved_chat_df["line"] = saved_chat_df["line"].apply(lambda e : e.lower())
    saved_chat_df['line'] = saved_chat_df['line'].apply(lambda e : e.replace("to  aisha qureshi(privately)",""))
    saved_chat_df['line'] = saved_chat_df['line'].apply(lambda e : e.replace("to  aisha qureshi(direct message)",""))

    l = saved_chat_df['line'].apply(lambda e : e.split(' : '))
    saved_chat_df['name'] =  l.str[0].str.split(" from ").str[1].str.strip()
    saved_chat_df['message'] =  l.str[1].str.strip()
    saved_chat_df = saved_chat_df.dropna()

    present_rows = saved_chat_df[saved_chat_df['message'].apply(lambda e : is_present(e))].copy()
    present_rows["is_present"]  = present_rows["message"].apply(lambda e : 1)
    present_rows.drop(columns=['line', 'message'], inplace=True)
    present_rows.drop_duplicates(inplace = True)

    present_rows = present_rows[["name", "is_present"]].set_index('name')

    # Read class names file
    class_names = pd.read_csv (STUDENT_NAMES_PATH, header = None)
    # Do some pre-processing on the dataframe.
    class_names.columns = ['name']
    class_names["name"] = class_names["name"].str.strip()
    class_names["name"] = class_names["name"].apply(lambda e : e.lower())
    class_names = class_names.set_index('name')

    # Join the 2 dataframes.
    joined_df = class_names.join(present_rows, how="outer", on="name")
    joined_df['is_present'] = joined_df['is_present'].fillna(0).astype(int)
    # (joined_df)
    left_joined_df = class_names.join(present_rows, how="left", on="name")
    left_joined_df['is_present'] = left_joined_df['is_present'].fillna(0).astype(int)
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
    for STUDENT_NAMES_PATH in student_list :
        matches, joined_df = join_files(filepath, STUDENT_NAMES_PATH)
        matches_list.append(matches)
        joined_df_list.append(joined_df)

    max_matches = max(matches_list)
    max_joins_df = joined_df_list[matches_list.index(max_matches)]
    return(max_joins_df)

parser = argparse.ArgumentParser()

parser.add_argument('--saved_chat_directory', help = 'Directory to scan "meeting_saved_chat" files')
parser.add_argument('--output_file_name', help = 'File name of the output processed file')

args = parser.parse_args()

SAVED_CHAT_DIR = args.saved_chat_directory

for subdir, dirs, files in os.walk(SAVED_CHAT_DIR):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filepath.endswith("meeting_saved_chat.txt"):
            try :
                print ("Processing file : " + filepath)
                df = get_max_join(filepath)

                df.reset_index(inplace=True)
                df = df[["name", "is_present"]]

                df["name"] = df["name"].str.title()
                df = df.sort_values(by=['name'])
                df.drop_duplicates(inplace = True)
                print(df)
                output_file_name = filepath.replace("meeting_saved_chat.txt", "attendance_new.csv")
                print ("Writing output to file : " + output_file_name)
                # Write the result to out tables.
                df.to_csv(output_file_name, index = False)

            except Exception as e :
                print ("FAILED to process file " + filepath)
                print (str(e))
