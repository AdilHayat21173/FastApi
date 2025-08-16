# Pydantic is used because it makes data validation and parsing easy.
# It checks that the data you receive has the correct type (e.g., string, int, list).
# It can automatically convert data into the right type if possible.
# It ensures your application gets clean and reliable data before using it.

from pydantic import BaseModel
from typing import List,Dict

class Patient(BaseModel):
    
    id: int
    name: str
    age: int
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]


def update_patient_data(patient:Patient):
    
    print("Updating patient data...")
    print(patient.id)
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)


patient_info = {
    "id": 1,
    "name": "John Doe",
    "age": 30,
    "married": True,
    "allergies": ["penicillin", "nuts"],
    "contact_details": {
        "email": "john.doe@example.com",
        "phone": "123-456-7890"
    }
}

patient1 = Patient(**patient_info)
update_patient_data(patient1)


# Now required and Optional field  in pydantic 
# In Pydantic models, all fields are required by default. We can explicitly mark some fields as optional when certain information may not always be provided, while keeping others required when the data is essential.

# By default (no strict=True) → Pydantic will try to convert types automatically.
# Example: if you pass "72.5" (string), and the field is float, it will convert it to float (72.5) instead of error.

# With strict=True → Pydantic will not convert automatically.
# Example: if you pass "72.5" (string), but the field is float with strict=True, it will raise a validation error ❌ because it’s not already a float.


from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Student(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the student', description='Enter the student name (max 50 chars)', examples=['Ali Khan', 'Sara Ahmed'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=5, lt=100, description="Age must be between 6 and 99")
    weight: Annotated[float, Field(gt=0, strict=True)]
    enrolled: Annotated[bool, Field(default=None, description='Is the student currently enrolled?')]
    subjects: Annotated[Optional[List[str]], Field(default=None, max_length=10, description="List of subjects student is studying")]
    contact_details: Dict[str, str]


def update_student_data(student: Student):
    print("Updating student data...")
    print(student.name)
    print(student.age)
    print(student.subjects)
    print(student.enrolled)
    print(student.email)
    print(student.weight)
    print(student.linkedin_url)



student_info = {
    'name': 'Ali Khan',
    'email': 'ali@example.com',
    'linkedin_url': 'http://linkedin.com/in/alikhan',
    'age': '20',
    'weight': 68.5,
    'contact_details': {'phone': '123456789'}
}

student1 = Student(**student_info)

update_student_data(student1)
