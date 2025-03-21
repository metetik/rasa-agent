from pydantic import BaseModel
import requests


class Patient(BaseModel):
    identity_number: str
    first_name: str
    last_name: str
    age: int

def get_patients():
	response = requests.get(f"http://localhost:8000/api/v0/patient/")

	if response.status_code == 200:
		return response.json()
	else:
		return []


def add_patient(patient: Patient):
	response = requests.post(f"http://localhost:8000/api/v0/patient/", json=patient.dict())

	if response.status_code == 201:
		return True
	else:
		return False