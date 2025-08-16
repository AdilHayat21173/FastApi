# In Pydantic v2, field_validator is used for two main purposes:

# Validation (checking a field):
# You can make rules for a field’s value.
# Example: If you are collecting student data for a contract with an academy like UET, you can check that the email must end with @uet.com. If someone enters a Gmail or Yahoo email, Pydantic will raise an error.

# Transformation (changing a field):
# You can automatically modify the value before saving it.
# Example: If the student writes their name in lowercase like "ali khan", you can transform it into "Ali Khan" using a validator.


from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains = ['uet.com', 'faysalbank.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value
    
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 and 100')


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'adil', 'email':'abc@uet.com', 'age': '30', 'weight': 75.2, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info) # validation -> type coercion

update_patient_data(patient1)





# Before mode (mode="before")

# Runs before Pydantic does type conversion.

# You can clean or transform raw input data.

# Example: If someone sends "25" (string) for age, the validator in before mode will see it as "25" (a string), not as an integer yet.
    

# After mode (mode="after")

# Runs after Pydantic has converted the type.

# You work with already validated/converted values.

# Example: If "25" (string) is given for age, Pydantic first converts it to 25 (integer), then the after validator will see it as an integer