#FastAPI Task Management System

The final project for building a complete FastAPI backend that manages tasks through a RESTful API- **Adele Alsaed**

#Features:
* **Data Storage:** uses the JSON Lines format in a simple '.txt' file for data presistance across server restarts.
* **Core Endpoint:** includes endpoints to Create, Read, Update, and Delete tasks.
* **Advanced Endpoints:** includes task filtering and task statistics (total, completed, pending, and completion percentage). 

#How to Run:
1. **install requirments:** 'pip install fastapi uvicorn'
2. **run the server:** 'uvicorn main:app --reload'
3. **open** the interactive API documentation at: 'http://127.0.0.1:8000/docs'
