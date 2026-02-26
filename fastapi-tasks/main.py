from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse #for export functionality
import json
import os
from storage import load_tasks, save_tasks

app = FastAPI()

#use | for optional description (defaulting to None if user doesn't provide one)
class Task(BaseModel):
    id: int
    title: str
    description: str | None= None
    completed: bool = False

class TaskCreate(BaseModel):
    title: str
    description: str | None= None

@app.get("/")
def read_root():
    return {"message": "Task Management API is running"}


@app.post("/tasks")
def create_task(task: TaskCreate):
    #load existing tasks
    tasks= load_tasks()
    
    #auto-generate ID (starting with 1)
    new_id= 1
    if len(tasks) > 0:
        new_id= max(t["id"] for t in tasks)+ 1

    #to create the new task dictionary
    new_task= {
        "id": new_id,
        "title": task.title,
        "description": task.description,
        "completed": False
    }

    #add to the list and save back
    tasks.append(new_task)
    save_tasks(tasks)

    return new_task


@app.get("/tasks")
def get_all_tasks(completed: bool | None= None):
    #simply load from file and return
    tasks= load_tasks()

    #if user provide T/F value, filter list
    if completed is not None:
        filtered_tasks= [task for task in tasks if task["completed"] == completed]
        return filtered_tasks
    
    #otherwise, return all
    return tasks


@app.get("/tasks/stats")
def get_task_stats():
    tasks= load_tasks()
    total= len(tasks)

    completed_count= sum(1 for task in tasks if task["completed"])
    pending_count= total - completed_count

    #calc.% (no division by 0!)
    percentage= (completed_count / total *100) if total > 0 else 0

    return{
        "total_tasks": total,
        "completed_tasks": completed_count,
        "pending_tasks": pending_count,
        "completion_percentage": round(percentage, 2)
    }


#check if file exists to avoid server errors
@app.get("/tasks/export")
def export_tasks():
    if not os.path.exists("tasks.txt"):
        raise HTTPException(status_code=404, detail="No tasks file available to export")
    #return file as downladable attachement
    return FileResponse(
        path= "tasks.txt",
        filename= "exported_tasks.json",
        media_type= "application/json"
    )

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    tasks= load_tasks()

    #go through tasks to find a match
    for task in tasks:
        if task["id"] == task_id:
            return task
    #no task found-error message Task not found
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks= load_tasks()

    for i, task in enumerate(tasks):
        del tasks[i] #remove task from the list
        save_tasks(tasks) #save updated list
        return {"message": "Task deleted successfully"}
    #no task found-error message
    raise HTTPException(status_code=404, detail= "Task not found")


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    tasks= load_tasks()

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
        #replace old data with new data
            tasks[i]= {
                "id": task_id, #same id
                "title": updated_task.title,
                "description:": updated_task.description,
                "completed": updated_task.completed
            }
            save_tasks(tasks)
            return tasks[i]
    
    #no task found- error message
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks")
def delete_all_tasks():
    save_tasks([]) #overwrite the file with an empty list
    return {"messsage": "All tasks deleted successfully"}
