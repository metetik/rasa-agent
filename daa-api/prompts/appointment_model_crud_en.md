**Role:** Sen FASTApi konusunda uzman bir yazılımcısın.

**Task:** Görevin sana verilen bilgiler çerçevesinde en iyi standartlara uygun fastapi kodları yazmaktır.

**Instruction:** Patient yazılan model class'larından ve route fonksiyonlarından faydalanarak Appointment için route fonksiyonlarını yaz.

* models: 
```
class Staff(SQLModel, table=True):
    """Represents a staff member in the clinic."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    surname: str
    role: str
    patient_notes: List["PatientNote"] = Relationship(back_populates="created_by")
    appointments: List["Appointment"] = Relationship(back_populates="dentist")


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
```
* routes:
```
from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app.database import get_session
from app.models import Patient
from fastapi import FastAPI
from pydantic import BaseModel

router = APIRouter(tags=["patient"])


@router.post("/patient/", response_model=schemas.PatientGetResponse, status_code=201)
async def create_patient(patient: schemas.PatientCreate, db_session=Depends(get_session)):
    """
    Creates a new Patient record.

    **Parameters:**
        - patient (schemas.PatientCreate): The Patient data to create.  Must include identity_number, name, surname, age.

    **Returns:**
        - The created Patient object on success.

    **Raises:**
        - HTTPException: 400 Bad Request if the request body is invalid or if there's a database error.
    """
    try:
        new_patient = Patient(**patient.model_dump())
        db_session.add(new_patient)
        db_session.commit()
        db_session.refresh(new_patient)
        return new_patient
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/patient/", response_model=list[schemas.PatientGetResponse])
async def list_patients(db_session=Depends(get_session)):
    """
    Retrieves a list of all Patient records.

    **Parameters:**
        - None

    **Returns:**
        - A list of Patient objects on success.

    **Raises:**
        - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        patient = db_session.query(Patient).all()
        return patient
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patient/{patient_id}", response_model=schemas.PatientGetResponse)
async def read_patient(patient_id: int, db_session=Depends(get_session)):
    """
    Retrieves a single Patient record by ID.

    **Parameters:**
        - patient_id (int): The ID of the Patient to retrieve.

    **Returns:**
        - The Patient object on success.

    **Raises:**
        - HTTPException: 404 Not Found if the Patient with the given ID does not exist.
        - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        patient = db_session.query(Patient).filter(Patient.id == patient_id).first()
        if patient is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/patient/{patient_id}", response_model=schemas.PatientGetResponse)
async def update_patient(patient_id: int, patient: schemas.PatientUpdate, db_session=Depends(get_session)):
    """
    Updates an existing Patient record.

    **Parameters:**
        - patient_id (int): The ID of the Patient to update.
        - patient (schemas.PatientUpdate): The updated Patient data.

    **Returns:**
        - The updated Patient object on success.

    **Raises:**
        - HTTPException: 404 Not Found if the Patient with the given ID does not exist.
        - HTTPException: 400 Bad Request if the request body is invalid or if there's a database error.
    """
    try:
        existing_patient = db_session.query(Patient).filter(Patient.id == patient_id).first()
        if existing_patient is None:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Update the existing patient with the new data
        for key, value in patient.model_dump():
            setattr(existing_patient, key, value)

        db_session.commit()
        db_session.refresh(existing_patient)
        return existing_patient
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/patient/{patient_id}", status_code=204)
async def delete_patient(patient_id: int, db_session=Depends(get_session)):
    """
    Deletes a Patient record.

    **Parameters:**
        - patient_id (int): The ID of the Patient to delete.

    **Returns:**
        - None on success.

    **Raises:**
        - HTTPException: 404 Not Found if the Patient with the given ID does not exist.
        - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        patient = db_session.query(Patient).filter(Patient.id == patient_id).first()
        if patient is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        db_session.delete(patient)
        db_session.commit()
        return
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
```