import json
import os

FILE_NAME= "tasks.txt"

def load_tasks():
    #check if file exists
    if not os.path.exists(FILE_NAME):
        return[]
    
    tasks= []
    #read file, parse json lines, return list of dictionaties 
    with open(FILE_NAME, "r") as file:
        for line in file:
            if line.strip():
                tasks.append(json.loads(line.strip()))
    return tasks

def save_tasks(tasks):
    #open file in write mode
    with open(FILE_NAME, "w") as file:
        #iterate through each task, converting it to json and writing it as a single line
        for task in tasks:
            file.write(json.dumps(task)+ "\n")
