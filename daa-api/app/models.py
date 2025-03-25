from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship, Table, Column
from datetime import datetime


class Staff(SQLModel, table=True):
    """Represents a staff member in the clinic."""
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    role: str
    patient_notes: List["PatientNote"] = Relationship(back_populates="created_by")
    appointments: List["Appointment"] = Relationship(back_populates="dentist")
    notifications: List["Notification"] = Relationship(back_populates="staff")
    treatments: List["Treatment"] = Relationship(back_populates="dentist")
    payment_plans: List["PaymentPlan"] = Relationship(back_populates="created_by")


class Agent(SQLModel, table=True):
    """Represents an agent used by the system."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    model: str
    treatments: List["Treatment"] = Relationship(back_populates="agent")
    treatment_notes: List["TreatmentNotes"] = Relationship(back_populates="agent")


class Patient(SQLModel, table=True):
    """Represents a patient in the clinic."""
    id: Optional[int] = Field(default=None, primary_key=True)
    identity_number: str
    first_name: str
    last_name: str
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
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
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
    dentist_id: int = Field(foreign_key="staff.id")
    agent_id: Optional[int] = Field(default=None, foreign_key="agent.id")
    name: str
    description: str
    cost: float
    status: str
    treatment_plan: Optional[TreatmentPlan] = Relationship(back_populates="treatments")
    patient: Optional["Patient"] = Relationship(back_populates="treatments")
    dentist: Optional["Staff"] = Relationship(back_populates="treatments")
    agent: Optional["Agent"] = Relationship(back_populates="treatments")
    treatment_notes: List["TreatmentNotes"] = Relationship(back_populates="treatment")
    images: List["Image"] = Relationship(back_populates="treatment")
    modified_date: datetime = Field(default_factory=datetime.now)


class TreatmentNotes(SQLModel, table=True):
    """Represents notes associated with a treatment."""
    id: Optional[int] = Field(default=None, primary_key=True)
    treatment_id: int = Field(foreign_key="treatment.id")
    agent_id: int = Field(foreign_key="agent.id")
    content: str
    created_date: datetime = Field(default_factory=datetime.now)
    modified_date: datetime = Field(default_factory=datetime.now)
    treatment: Optional["Treatment"] = Relationship(back_populates="treatment_notes")
    agent: Optional["Agent"] = Relationship(back_populates="treatment_notes")


class PaymentPlan(SQLModel, table=True):
    """Represents a payment plan for a patient."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    created_by_id: int = Field(foreign_key="staff.id")  # Renamed from created_by
    total_amount: float
    paid_amount: float
    remaining_amount: float
    status: str
    description: str
    created_date: datetime = Field(default_factory=datetime.now)
    modified_date: datetime = Field(default_factory=datetime.now)
    patient: Optional["Patient"] = Relationship(back_populates="payment_plans")
    created_by: Optional["Staff"] = Relationship(back_populates="payment_plans")
    payments: List["Payment"] = Relationship(back_populates="payment_plan")


class Payment(SQLModel, table=True):
    """Represents a payment made towards a payment plan."""
    id: Optional[int] = Field(default=None, primary_key=True)
    payment_plan_id: int = Field(foreign_key="paymentplan.id")  # Add foreign key
    status: str
    operation: str
    amount: float
    date: datetime = Field(default_factory=datetime.now)  # Use default_factory
    payment_plan: Optional["PaymentPlan"] = Relationship(back_populates="payments")  # Fix relationship


class Image(SQLModel, table=True):
    """Represents an image associated with a patient or treatment."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    treatment_id: Optional[int] = Field(default=None, foreign_key="treatment.id")
    url: str
    description: Optional[str] = None
    created_date: datetime = Field(default_factory=datetime.now)
    patient: Optional["Patient"] = Relationship(back_populates="images")
    treatment: Optional["Treatment"] = Relationship(back_populates="images")


class Notification(SQLModel, table=True):
    """Represents a notification for a patient or staff."""
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    staff_id: int = Field(foreign_key="staff.id")
    message: str
    date: datetime = Field(default_factory=datetime.now)
    read: bool = False
    patient: Optional["Patient"] = Relationship(back_populates="notifications")
    staff: Optional["Staff"] = Relationship(back_populates="notifications")

