# zoom-attendance

Download this code from : \
```git clone https://github.com/zeeshanin12/zoom-attendance.git```

This python program does some data processing on chats saved from Zoom. It parses the input text files, and finds the students to wrote "present". And then creates an output file that has a list of all the students with 1 marked is present and 0 is absent.

This function takes the following 3 input arguments :

1) ```--saved_chat_path``` : The saved zoom chat file path. This is the input file to process.

2) ```--class_names_path``` : File path containing list of all students in the class. The output list will have the names of all student in this file with attendance marked from the input file(--saved_chat_path).

3) ```--output_file_name``` : File name of the output processed file. This file is saved in the directory from which the program is run.


For example : \
```python main.py --saved_chat_path ./saved_chat.txt --class_names_path ./class_10d.csv --output_file_name out.txt ```
