from pydantic import BaseModel
import requests

API_BASE = "http://localhost:8000/api/v0"

class Patient(BaseModel):
    identity_number: str
    first_name: str
    last_name: str
    age: int


def get_patients():
    response = requests.get(f"{API_BASE}/patient/")

    if response.status_code == 200:
        return response.json()
    else:
        return []


def add_patient(patient: Patient):
    response = requests.post(f"{API_BASE}/patient/", json=patient.dict())

    if response.status_code == 201:
        return True
    else:
        return False


def find_patient(first_name: str, last_name: str, identity_number: str | None):
    response = requests.get(f"{API_BASE}/patient/name/", params={"first_name": first_name, "last_name": last_name})

    if response.status_code == 200:
        return response.json()
    else:
        response = requests.get(f"{API_BASE}/patient/" + str(identity_number))
        if response.status_code == 200:
            return response.json()
    
    return None