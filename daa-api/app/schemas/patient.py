from pydantic import BaseModel
from typing import Optional


class PatientBase(BaseModel):
    identity_number: str
    first_name: str
    last_name: str
    age: int


class PatientCreate(PatientBase):
    id: int


class PatientUpdate(PatientBase):
    id: int


class PatientPatch(PatientBase):
    id: int


class PatientGetResponse(PatientBase):
    id: int