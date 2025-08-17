from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Optional, Annotated, Literal
import json
from typing import Dict

app = FastAPI()

class Address(BaseModel):
    city: Annotated[str, Field(..., description='City of the student')]
    state: Annotated[str, Field(..., description='State of the student')]

class Admission(BaseModel):
    id: Annotated[str, Field(..., description='ID of the student')]  # Changed to str to match usage
    first_name: Annotated[str, Field(..., description='First name of the student')]
    last_name: Annotated[str, Field(..., description='Last name of the student')]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description='Gender of the student')]
    date_of_birth: Annotated[str, Field(..., description='Date of birth of the student')]
    class_applied: Annotated[str, Field(..., description='Class applied for')]
    height_cm: Annotated[float, Field(..., gt=0, description='Height of the student in cm')]
    weight_kg: Annotated[float, Field(..., gt=0, description='Weight of the student in kg')]
    father_name: Annotated[str, Field(..., description='Father name of the student')]
    contact_number: Annotated[str, Field(..., description='Contact number of the student')]
    address: Address
    status: Annotated[str, Field(..., description='Admission status of the student')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight_kg / ((self.height_cm / 100) ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'  # Fixed: was 'Normal' for overweight range
        else:
            return 'Obese'

def load_data():
    try:
        with open('school_admission.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}  # Return empty dict if file doesn't exist
    except json.JSONDecodeError:
        return {}  # Return empty dict if JSON is invalid

def save_data(data):
    with open('school_admission.json', 'w') as f:
        json.dump(data, f, indent=2)

@app.get("/")
def hello():
    return {'message': 'Student Admission Management System API'}

@app.get("/about")
def about():
    return {'message': 'A fully functional API to manage your student admission records'}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/student/{student_id}")
def view_student(student_id: str = Path(..., description="ID of the student in the DB", example="S001")):
    data = load_data()

    if student_id in data:
        return data[student_id]
    raise HTTPException(status_code=404, detail="Student not found")

@app.get('/sort')
def sort_student(
    sort_by: str = Query(..., description='Sort on the basis of height_cm, weight_kg or bmi'), 
    order: str = Query('asc', description='sort in asc or desc order')
):
    valid_fields = ['height_cm', 'weight_kg', 'bmi']  # Fixed field names to match model

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    if not data:
        return []

    sort_order = True if order == 'desc' else False

    # Create Admission objects to access computed fields like bmi
    students_list = []
    for student_id, student_data in data.items():
        try:
            # Add the id back to the data for proper object creation
            student_data_with_id = {**student_data, 'id': student_id}
            admission = Admission(**student_data_with_id)
            
            # Get the sort value
            if sort_by == 'bmi':
                sort_value = admission.bmi
            else:
                sort_value = getattr(admission, sort_by)
            
            students_list.append({
                'student_id': student_id,
                'data': admission.model_dump(),
                'sort_value': sort_value
            })
        except Exception as e:
            # Skip invalid records
            continue

    sorted_data = sorted(students_list, key=lambda x: x['sort_value'], reverse=sort_order)
    
    # Return just the student data
    return [item['data'] for item in sorted_data]

@app.post('/create')
def create_student(student: Admission):  # Fixed: was 'Patient' instead of 'Admission'
    # load existing data
    data = load_data()

    # check if the student already exists
    if student.id in data:
        raise HTTPException(status_code=400, detail='Student already exists')

    # new student add to the database
    data[student.id] = student.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message': 'Student created successfully'})




class StudentUpdate(BaseModel):
    first_name: Annotated[Optional[str], Field(default=None, description='First name of the student')]
    last_name: Annotated[Optional[str], Field(default=None, description='Last name of the student')]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None, description='Gender of the student')]
    date_of_birth: Annotated[Optional[str], Field(default=None, description='Date of birth of the student')]
    class_applied: Annotated[Optional[str], Field(default=None, description='Class applied for')]
    height_cm: Annotated[Optional[float], Field(default=None, gt=0, description='Height of the student in cm')]
    weight_kg: Annotated[Optional[float], Field(default=None, gt=0, description='Weight of the student in kg')]
    father_name: Annotated[Optional[str], Field(default=None, description='Father name of the student')]
    contact_number: Annotated[Optional[str], Field(default=None, description='Contact number of the student')]
    city: Annotated[Optional[str], Field(default=None, description='City of the student')]
    state: Annotated[Optional[str], Field(default=None, description='State of the student')]
    status: Annotated[Optional[str], Field(default=None, description='Admission status of the student')]

@app.put('/edit/{student_id}')
def update_student(student_id: str, student_update: StudentUpdate):
    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=404, detail='Student not found')
    
    existing_student_info = data[student_id]

    updated_student_info = student_update.model_dump(exclude_unset=True)

    # Handle address updates separately
    address_updates = {}
    if 'city' in updated_student_info:
        address_updates['city'] = updated_student_info.pop('city')
    if 'state' in updated_student_info:
        address_updates['state'] = updated_student_info.pop('state')

    # Update the main student info
    for key, value in updated_student_info.items():
        existing_student_info[key] = value

    # Update address if needed
    if address_updates:
        if 'address' not in existing_student_info:
            existing_student_info['address'] = {}
        existing_student_info['address'].update(address_updates)

    # Create pydantic object to recalculate BMI and verdict
    existing_student_info['id'] = student_id
    student_pydantic_obj = Admission(**existing_student_info)
    
    # Convert back to dict and remove id
    existing_student_info = student_pydantic_obj.model_dump(exclude=['id'])

    # Save updated data
    data[student_id] = existing_student_info

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Student updated successfully'})

@app.delete('/delete/{student_id}')
def delete_student(student_id: str):
    # load data
    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=404, detail='Student not found')
    
    del data[student_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Student deleted successfully'})