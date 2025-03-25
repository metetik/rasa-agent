from typing import Any, Dict, List, Text
from datetime import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.services.patient_services import add_patient, get_patients, Patient, find_patient
from actions.services.staff_services import find_dentist
from actions.services.appointment_services import add_appointment, get_appointments, check_dentist_availability, Appointment
from actions.services.data_conversion import parse_datetime

class CreateAppointment(Action):
    def name(self) -> str:
        return "create_appointment"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        patient_first_name = tracker.get_slot("create_appointment_patient_first_name")
        patient_last_name = tracker.get_slot("create_appointment_patient_last_name")
        dentist_first_name = tracker.get_slot("create_appointment_dentist_first_name")
        dentist_last_name = tracker.get_slot("create_appointment_dentist_last_name")
        appointment_start_date_str = tracker.get_slot("create_appointment_start_date")
        # patient_identity_number = tracker.get_slot("create_appointment_patient_identity_number")
        # appointment_description = tracker.get_slot("create_appointment_description")
        # appointment_end_date = tracker.get_slot("create_appointment_end_date")
        appointment_idenity_number = None
        appointment_description = None
        appointment_end_date_str = None

        
        appointment_start_date = parse_datetime(appointment_start_date_str)
        appointment_end_date = parse_datetime(appointment_end_date_str) if appointment_end_date_str is not None else None



        if not isinstance(appointment_start_date, datetime):
            return [SlotSet("return_value", "invalid_data")]
        else:
            appointment_start_date_iso = appointment_start_date.isoformat()
        
        patient = find_patient(patient_first_name, patient_last_name, appointment_idenity_number)
        if patient is None:
            return [SlotSet("return_value", "patient_not_found")]

        dentist = find_dentist(dentist_first_name, dentist_last_name)
        if dentist is None:
            return [SlotSet("return_value", "dentist_not_found")]

        is_dentist_available = check_dentist_availability(dentist, appointment_start_date, appointment_end_date)
        if not is_dentist_available:
            return [SlotSet("return_value", "dentist_unavailable")]

        new_appointment = Appointment(patient_id=patient["id"],
            dentist_id=dentist["id"],
            start_date=appointment_start_date_iso,
            end_date=appointment_end_date,
            description=appointment_description)
        
        result = add_appointment(new_appointment)
        if result:
            return [SlotSet("return_value", "success")]
        else:
            return [SlotSet("return_value", "failed")]
