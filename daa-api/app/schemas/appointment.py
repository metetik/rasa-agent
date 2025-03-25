from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class AppointmentBase(BaseModel):
    patient_id: int
    dentist_id: int
    start_date: str | datetime
    end_date: Optional[str | datetime] = None
    description: Optional[str] = None
    completed: Optional[bool] = False

class AppointmentCreate(AppointmentBase):
    id: Optional[int] = None


class AppointmentUpdate(AppointmentBase):
    id: int


class AppointmentGetResponse(AppointmentBase):
    id: int