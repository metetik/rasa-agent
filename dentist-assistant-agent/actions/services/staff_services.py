from pydantic import BaseModel
import requests

API_BASE = "http://localhost:8000/api/v0"

class Staff(BaseModel):
    first_name: str
    last_name: str
    role: str

def find_dentist(first_name: str, last_name: str):
    response = requests.get(f"{API_BASE}/staff/dentist/name/", params={"first_name": first_name, "last_name": last_name})

    if response.status_code == 200:
        return response.json()
    else:
        return None