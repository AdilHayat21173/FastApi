# Serialization = converting a Pydantic model into dict or JSON.
# model_dump() → Python dict
# model_dump_json() → JSON string
# Options:
# exclude_unset=True → skip fields not given by user
# exclude_defaults=True → skip fields equal to default
# exclude_none=True → skip fields with None

from pydantic import BaseModel

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'adil', 'age': 35, 'address': address1}

patient1 = Patient(**patient_dict)

temp = patient1.model_dump(exclude_unset=True)

print(temp)
print(type(temp))



