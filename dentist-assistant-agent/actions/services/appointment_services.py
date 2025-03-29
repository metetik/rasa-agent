from pydantic import BaseModel
from actions.services.patient_services import Patient
import requests
from datetime import datetime, timedelta
from typing import Optional

API_BASE = "http://localhost:8000/api/v0"

class Appointment(BaseModel):
    patient_id: int
    dentist_id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    completed: Optional[bool] = False

def get_appointments():
    response = requests.get(f"{API_BASE}/appointment/")

    if response.status_code == 200:
        return response.json()
    else:
        return []


def get_appointments_by_patient(patient_id: int):
    """
    Retrieves all appointments for a specific patient.
    Args:
        patient_id: ID of the patient.
    Returns:
        A list of Appointment objects.
    """
    response = requests.get(f"{API_BASE}/appointment/patient/{patient_id}")

    if response.status_code == 200:
        return response.json()
    else:
        return []

def add_appointment(appointment: Appointment):
    payload = appointment.dict()

    payload["start_date"] = payload["start_date"].isoformat()
    payload["end_date"] = payload["end_date"].isoformat() if payload["end_date"] is not None else None

    response = requests.post(f"{API_BASE}/appointment/", json=payload)

    if response.status_code == 201:
        return True
    else:
        return False

def check_dentist_availability(dentist, start_date, end_date):
    """
    Checks if the dentist is available within the specified date range.

    Args:
        dentist: Dictionary containing dentist information.
        start_date: Start date to check (in ISO format).
        end_date: End date to check (in ISO format, can be None).

    Returns:
        A boolean value indicating whether the dentist is available.
    """

    try:
        response = requests.get(f"{API_BASE}/appointment/dentist/{dentist['id']}")
        dentist_appointments = response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return False  # If the API request fails, assume not available

    if end_date is None:
        end_date = start_date + timedelta(minutes=30)

    if response.status_code == 200:
        for appointment in dentist_appointments:
            try:
                appointment_start = datetime.fromisoformat(appointment["start_date"])
            except ValueError:
                print(f"Invalid date format: {appointment['start_date']}")
                continue  # Skip to the next appointment if the date format is invalid
            
            try:
                appointment_end = datetime.fromisoformat(appointment["end_date"])
            except (ValueError, TypeError):
                print(f"Invalid date format: {appointment['end_date']}")
                
                # If end_date is not provided, assume the appointment lasts 30 minutes
                if appointment["end_date"] is None:
                    appointment_end = appointment_start + timedelta(minutes=30)
                else:
                    continue  # Skip to the next appointment if the date format is invalid


            # Check with start and end dates of the appointment
            # print(start_date, end_date, appointment_start, appointment_end)
            if not ((start_date < appointment_start and end_date <= appointment_start) \
                or (start_date >= appointment_end and end_date > appointment_end)):
                return False # Not available if the appointment overlaps with the requested time

            # If no overlap is found, the dentist is available for this appointment
            # Continue to the next appointment

        # If all appointments are checked and no overlap is found, the dentist is available
        return True

    else:
        # If the API request fails, assume not available
        return False