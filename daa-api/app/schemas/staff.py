from pydantic import BaseModel
from typing import Optional

class StaffBase(BaseModel):
    first_name: str
    last_name: str
    role: str

class StaffCreate(StaffBase):
    id: int


class StaffUpdate(StaffBase):
    id: int

class StaffPatch(StaffBase):
    id: int


class StaffGetResponse(StaffBase):
    id: int