from fastapi import APIRouter, Depends, HTTPException
from app import schemas
from app.database import get_session
from app.models import Staff, Appointment, Patient
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session

router = APIRouter(tags=["appointment"])

@router.post("/appointment/", response_model=schemas.AppointmentGetResponse, status_code=201)
async def create_appointment(appointment: schemas.AppointmentCreate, db_session: Session=Depends(get_session)):
    """
    Creates a new Appointment record.

    **Parameters:**
    - appointment (schemas.AppointmentCreate): The Appointment data to create. Must include patient_id, dentist_id, description, start_date, and end_date.
    
    **Returns:**
    - The created Appointment object on success.
    
    **Raises:**
    - HTTPException: 400 Bad Request if the request body is invalid or if there's a database error.
    - HTTPException: 404 Not Found if the patient or dentist does not exist.
    """
    try:
        # Validate that patient and dentist exist
        patient = db_session.query(Patient).filter(Patient.id == appointment.patient_id).first()
        dentist = db_session.query(Staff).filter(Staff.id == appointment.dentist_id).first()
        
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        if not dentist:
            raise HTTPException(status_code=404, detail="Dentist not found")
        if not appointment.start_date:
            raise HTTPException(status_code=400, detail="Invalid start_date")

        new_appointment = Appointment(
            patient_id=appointment.patient_id,
            dentist_id=appointment.dentist_id,
            description=appointment.description,
            start_date=datetime.fromisoformat(appointment.start_date) if appointment.start_date else None,
            end_date=datetime.fromisoformat(appointment.end_date) if appointment.end_date else None,
            completed=appointment.completed
        )
        db_session.add(new_appointment)
        db_session.commit()
        db_session.refresh(new_appointment)

        return new_appointment
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/appointment/patient/{patient_id}", response_model=list[schemas.AppointmentGetResponse])
async def get_appointments_by_patient(patient_id: int, db_session: Session=Depends(get_session)):
    """
    Retrieves all appointments for a specific patient.
    
    **Parameters:**
    - patient_id (int): The ID of the patient.
    
    **Returns:**
    - A list of Appointment objects.
    
    **Raises:**
    - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        appointments = db_session.query(Appointment).filter(Appointment.patient_id == patient_id).all()
        if appointments is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return appointments
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/appointment/dentist/{dentist_id}", response_model=list[schemas.AppointmentGetResponse])
async def get_appointments_by_dentist(dentist_id: int, db_session: Session = Depends(get_session)):
    """
    Retrieves all appointments for a specific dentist.

    **Parameters:**
    - dentist_id (int): The ID of the dentist.

    **Returns:**
    - A list of Appointment objects.

    **Raises:**
    - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        appointments = db_session.query(Appointment).filter(Appointment.dentist_id == dentist_id).all()
        if appointments is None:
            return []
        return appointments
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/appointment/{appointment_id}", response_model=schemas.AppointmentGetResponse)
async def get_appointment(appointment_id: int, db_session: Session=Depends(get_session)):
    """
    Retrieves a specific appointment by ID.
    
    **Parameters:**
    - appointment_id (int): The ID of the appointment.
    
    **Returns:**
    - The Appointment object on success.
    
    **Raises:**
    - HTTPException: 404 Not Found if the appointment does not exist.
    - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        appointment = db_session.query(Appointment).filter(Appointment.id == appointment_id).first()
        if appointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return appointment
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/appointment/{appointment_id}", response_model=schemas.AppointmentGetResponse)
async def update_appointment(appointment_id: int, appointment: schemas.AppointmentUpdate, db_session: Session=Depends(get_session)):
    """
    Updates an existing Appointment record.
    
    **Parameters:**
    - appointment_id (int): The ID of the appointment to update.
    - appointment (schemas.AppointmentUpdate): The updated Appointment data.
    
    **Returns:**
    - The updated Appointment object on success.
    
    **Raises:**
    - HTTPException: 404 Not Found if the appointment does not exist.
    - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        existing_appointment = db_session.query(Appointment).filter(Appointment.id == appointment_id).first()
        if existing_appointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")

        # Update the existing appointment with the new data
        for key, value in appointment.model_dump(exclude_unset=True).items():
            if key == "start_time":
                setattr(existing_appointment, key, datetime.fromisoformat(value))
            elif key == "end_time":
                setattr(existing_appointment, key, datetime.fromisoformat(value))
            else:
                setattr(existing_appointment, key, value)

        db_session.commit()
        db_session.refresh(existing_appointment)
        return existing_appointment
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/appointment/{appointment_id}")
async def delete_appointment(appointment_id: int, db_session: Session=Depends(get_session)):
    """
    Deletes an appointment.
    
    **Parameters:**
    - appointment_id (int): The ID of the appointment to delete.
    
    **Raises:**
    - HTTPException: 404 Not Found if the appointment does not exist.
    - HTTPException: 500 Internal Server Error if there's a database error.
    """
    try:
        appointment = db_session.query(Appointment).filter(Appointment.id == appointment_id).first()
        if appointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        db_session.delete(appointment)
        db_session.commit()
        return {"message": "Appointment deleted"}
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))