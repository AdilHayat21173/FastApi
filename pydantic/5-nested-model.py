# A nested model in Pydantic means you can use one model inside another model.
# Why we use it:
# Organized data → Instead of putting everything in one flat structure, we can group related fields together. For example, address details (city, state, pin) belong together, so we keep them inside an Address model.
# Reusability → The same Address model can be used for patients, students, employees, etc., without rewriting.
# Validation → Pydantic will validate both the main model and the nested model automatically. For example, if the pin is missing or invalid, the error will come from inside the nested model.
# Clarity → It makes the code easier to read and understand because each model has a clear purpose.

from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'adil', 'gender': 'male', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)
print(patient1.name)
print(patient1.address.city)

# give data format 
temp = patient1.model_dump(include={'address': {'city', 'state'}})

print(type(temp))
#give json format 
temp = patient1.model_dump_json()

print(type(temp))
