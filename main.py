import pandas as pd
from re import search
import sys
# python main.py ./saved_chat.txt out.txt ./class_10d.csv
def is_present (input) :
    if search("present", input) :
        return True
    else :
        return False

#INPUT_FILE_PATH = "./test.txt"
INPUT_FILE_PATH = sys.argv[1]
OUTPUT_FILE_PATH = sys.argv[2]
CLASS_NAME_FILE_PATH= sys.argv[3]

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

#joined_df["char"] = joined_df.index
#joined_df["char"]= joined_df["char"].apply(lambda e :len(e))
#joined_df.drop_duplicates()

print(joined_df)

# Write the result to out tables. 
joined_df.to_csv(OUTPUT_FILE_PATH, index = True)
