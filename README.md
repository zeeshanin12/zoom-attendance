# zoom-attendance

Download this code from : \
```git clone https://github.com/zeeshanin12/zoom-attendance.git```

This python program does some data processing on chats saved from Zoom. It parses the input text files, and finds the students to wrote "present". And then creates an output file that has a list of all the students with 1 marked is present and 0 is absent.

This function takes the following input argument :

```--saved_chat_directory``` : A directory path that contains the saved zoom chat files. All files named "meeting_saved_chat" in this directory will be processed.

Once processed, these files will be as attendance.csv



For example : \
```python main.py --saved_chat_directory /Users/khanz/aisha-attendance/ ```
