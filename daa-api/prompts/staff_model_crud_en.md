**Task:** Generate FastAPI CRUD (Create, Read, Update, Delete) endpoints for a SQLModel model.

**Context:**

* You are generating FastAPI endpoints for a backend API.
* The API uses SQLModel for database interaction.
* The generated endpoints should adhere to FastAPI best practices.

**Input:**
* **SQLModel Model Definition:** 
```python
# models.py
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship, Table, Column
from datetime import datetime


class Staff(SQLModel, table=True):
    """Represents a staff member in the clinic."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    role: str
    patient_notes: List["PatientNote"] = Relationship(back_populates="created_by")
    appointments: List["Appointment"] = Relationship(back_populates="dentist")


class Agent(SQLModel, table=True):
    """Represents an agent used by the system."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    model: str


class Patient(SQLModel, table=True):
    """Represents a patient in the clinic."""
    id: Optional[int] = Field(default=None, primary_key=True)
    identity_number: str
    name: str
    surname: str
    age: int
    treatment_plans: List["TreatmentPlan"] = Relationship(back_populates="patient")
    treatments: List["Treatment"] = Relationship(back_populates="patient")
    payment_plans: List["PaymentPlan"] = Relationship(back_populates="patient")
    appointments: List["Appointment"] = Relationship(back_populates="patient")
    patient_notes: List["PatientNote"] = Relationship(back_populates="patient")
    notifications: List["Notification"] = Relationship(back_populates="patient")
    images: List["Image"] = Relationship(back_populates="patient")


class PatientNote(SQLModel, table=True):
    """Represents a note associated with a patient."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    staff_id: int = Field(foreign_key="staff.id")
    note: str
    created_at: datetime
    patient: Optional[Patient] = Relationship(back_populates="patient_notes")
    created_by: Optional[Staff] = Relationship(back_populates="patient_notes")
    
class Appointment(SQLModel, table=True):
    """Represents an appointment for a patient."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    dentist_id: int = Field(foreign_key="staff.id")
    description: str
    start_date: datetime
    end_date: datetime
    completed: bool = False
    patient: Optional[Patient] = Relationship(back_populates="appointments")
    dentist: Optional[Staff] = Relationship(back_populates="appointments")


class TreatmentPlan(SQLModel, table=True):
    """Represents a treatment plan for a patient."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    description: str
    start_date: datetime
    end_date: datetime
    status: str
    treatments: List["Treatment"] = Relationship(back_populates="treatment_plan")
    patient: Optional["Patient"] = Relationship(back_populates="treatment_plans")


class Treatment(SQLModel, table=True):
    """Represents a treatment within a treatment plan."""
    id: Optional[int] = Field(default=None, primary_key=True)
    treatment_plan_id: int = Field(foreign_key="treatmentplan.id")
    patient_id: int = Field(foreign_key="patient.id")
    name: str
    description: str
    cost: float
    status: str
    treatment_plan: Optional[TreatmentPlan] = Relationship(back_populates="treatments")
    patient: Optional["Patient"] = Relationship(back_populates="treatments")
    dentist: int # Foreign key to Staff table (Dentist)
    agent: Relationship[Agent] = Relationship(back_populates="treatments")
    treatment_notes: Relationship["TreatmentNotes"] = Relationship(back_populates="treatments")
    modified_date: datetime = Field(default=datetime.now)


class TreatmentNotes(SQLModel, table=True):
    """Represents notes associated with a treatment."""
    id: Optional[int] = Field(default=None, primary_key=True)
    treatment: Relationship[Treatment] = Relationship(back_populates="treatment_notes")
    content: str
    created_date: datetime = Field(default=datetime.now)
    modified_date: datetime = Field(default=datetime.now)
    agent: Relationship[Agent] = Relationship(back_populates="treatment_notes")


class PaymentPlan(SQLModel, table=True):
    """Represents a payment plan for a patient."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    total_amount: float
    paid_amount: float
    remaining_amount: float
    status: str
    patient: Optional[Patient] = Relationship(back_populates="payment_plans")
    description: str
    created_by: int # Foreign key to Staff table (Creator)
    created_date: datetime = Field(default=datetime.now)
    modified_date: datetime = Field(default=datetime.now)
    payments: List["Payment"] = Relationship(back_populates="payment_plan")


class Payment(SQLModel, table=True):
    """Represents a payment made towards a payment plan."""
    id: Optional[int] = Field(default=None, primary_key=True)
    payment_plan: Relationship[PaymentPlan] = Relationship(back_populates="payments")
    status: str
    operation: str
    amount: float
    date: datetime = Field(default=datetime.now)


class Image(SQLModel, table=True):
    """Represents an image associated with a patient or treatment."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient: Relationship[Patient] = Relationship(back_populates="images")
    treatment: Relationship[Treatment] = Relationship(back_populates="images")
    url: str
    description: Optional[str] = None


class Notification(SQLModel, table=True):
    """Represents a notification for a patient or staff."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient: Relationship[Patient] = Relationship(back_populates="notifications")
    staff: int # Foreign key to Staff table
    message: str
    date: datetime = Field(default=datetime.now)
    read: bool = False
```

* **Model Name:** Staff


**Output:**

Generate a FastAPI endpoint definition (Python code) for the specified model. The code should:

* **Define Route Functions:** Create route functions for Create (POST), Read (GET - single and list), Update (PUT/PATCH), and Delete (DELETE) operations.
* **Include Docstrings:**  Each route function should have a clear and informative docstring explaining its purpose, parameters, and expected response. Use Markdown formatting within the docstrings for readability.
* **Handle Errors:** Implement error handling to catch potential issues (e.g., database connection errors, validation errors, resource not found) and return appropriate HTTP response codes (e.g., 400 Bad Request, 404 Not Found, 500 Internal Server Error) with informative error messages.
* **Follow FastAPI Best Practices:**  Utilize FastAPI's features like Pydantic models for request body validation, dependency injection, and path parameters.
* **Return Appropriate Responses:**  Return appropriate HTTP response codes (200 OK, 201 Created, 204 No Content) and data formats (JSON) for each operation.
* **Include Example Usage (Optional):**  Provide a brief example of how to use the endpoint in a `try...except` block.

**Example File Structure:**
```
my_project/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── staff.py
│   │   ├── agent.py 
│   │   └── ...
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── staff_schema.py
│   │   ├── agent_schema.py 
│   │   └── ...
│   ├── database.py 
│   ├── models.py
│   ├── main.py # Uygulama başlangıç noktası
└── ...
```

**Example route file:**

```python
from fastapi import APIRouter, Depends
from . import schemas
from ..database import get_session
from ..models import Staff
from fastapi import HTTPException
from pydantic import BaseModel

router = APIRouter()

@router.get("/staff/{staff_id}", response_model=schemas.staffGetResponse)
async def get_staff(staff_id: int, db=Depends(get_session)):
    # Fill here
    pass

```

**Example Docstring Format (Use this as a template):**

```python
"""
Creates a new [Model Name] record.

    **Parameters:**
        - [Parameter Name]: [Parameter Description] (required/optional)

    **Returns:**
        - [Model Name] object on success.
        - Error message on failure.

    **Raises:**
        - [Error Type]: [Error Description]
"""
```
**Important**: Replace the bracketed placeholders above with the specific details for the model you are working with. This prompt is designed to be reusable, so you only need to change the model name and definition.