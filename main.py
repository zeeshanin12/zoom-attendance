import pandas as pd
from re import search
import argparse, sys
# python main.py --saved_chat_path ./saved_chat.txt --output_file_name out.txt --class_names_path ./class_10d.csv
def is_present (input) :
    if search("present", input) :
        return True
    else :
        return False

parser = argparse.ArgumentParser()

parser.add_argument('--saved_chat_path', help = 'File path to the saved Zoom chat')
parser.add_argument('--class_names_path', help ='File path containing list of all students in the class')
parser.add_argument('--output_file_name', help = 'File name of the output processed file')

args = parser.parse_args()

INPUT_FILE_PATH = args.saved_chat_path
OUTPUT_FILE_NAME = args.output_file_name
CLASS_NAME_FILE_PATH = args.class_names_path

# Read input saved chat file.
df = pd.read_csv (INPUT_FILE_PATH, header = None)
# Do some pre-processing.
df.columns = ['line']
lines = df["line"].str.split("\t From ").str[1]
l = lines.apply(lambda e : e.split(' : '))
df['name'] =  l.str[0].apply(lambda e : e[1:].lower())
df['message'] =  l.str[1].apply(lambda e : e.lower())

df = df[['name', 'message']]
present_rows = df[df['message'].apply(lambda e : is_present(e))]

present_rows["is_present"]  = present_rows["message"].apply(lambda e : 1)
present_rows.drop_duplicates(inplace=True)
present_rows = present_rows[["name", "is_present"]].set_index('name')

print(present_rows)

# Read class names file
class_names = pd.read_csv (CLASS_NAME_FILE_PATH, header = None)

# Do some pre-processing on the dataframe.
class_names.columns = ['name']
class_names["name"] = class_names["name"].apply(lambda e : e.lower())
class_names = class_names.set_index('name')
#print (class_names)

# Join the 2 dataframes.
joined_df = class_names.join(present_rows, how="outer", on="name")

# Do some post processing
joined_df = joined_df.fillna(0).astype(int)
joined_df.index = joined_df.index.str.title()
joined_df.sort_index(inplace = True)

print(joined_df)

# Write the result to out tables.
joined_df.to_csv(OUTPUT_FILE_NAME, index = True)
