# In FastAPI, GET is used to retrieve data from the server.

from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import json
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "welcome to the fast api app to manage student data"}

@app.get("/hello")
def say_hello():
    return {"message": "Hello, World!"}



#Endpoint with retrieve all the data from database 
STUDENTS_FILE = "student.json"

# Function to load student data
def load():
    with open(STUDENTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
    
# Endpoint to get all students
@app.get("/view")
def view_students():
    return load()

# Endpoint to get a student by ID by parameter
@app.get("/students/{student_id}")
def get_student_by_id(student_id: str):
    students = load()
    if student_id in students:
        return students[student_id]
    else:
        raise HTTPException(status_code=404, detail="Student not found")
    


# Query Parameters in FastAPI
# Definition: Query parameters are used to pass additional information to an endpoint without changing its path.
# Purpose: Typically used for filtering, sorting, searching, and pagination.
# Key Points:
# They appear after ? in the URL.
# Multiple query parameters are separated by &.
# They are optional unless explicitly made required.
# They allow you to modify the data returned, not the endpoint path.

@app.get("/sort_students")
def sort_students(
    sort_by: str = Query(..., description="Sort by weight, cgpa, or age"),
    order: str = Query("asc", description="Sort in asc or desc order")
):
    valid_fields = ["weight", "cgpa", "age"]

    # Check if sort_by is valid
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Choose from {valid_fields}")

    # Check if order is valid
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Choose 'asc' or 'desc'")

    # Load data
    data = load()

    # Set reverse order for sorting
    reverse_order = True if order == "desc" else False

    # Sort the data
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=reverse_order)

    return sorted_data