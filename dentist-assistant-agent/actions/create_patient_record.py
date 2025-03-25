from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.services.patient_services import add_patient, get_patients, Patient 

class CreatePatientRecord(Action):
    def name(self) -> str:
        return "create_patient_record"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        patients = get_patients()
        patient_identity_number = tracker.get_slot("add_patient_identity_number")
        patient_first_name = tracker.get_slot("add_patient_first_name")
        patient_last_name = tracker.get_slot("add_patient_last_name")
        patient_age = tracker.get_slot("add_patient_age")

        if patient_identity_number is None:
            return [SlotSet("return_value", "data_not_present")]

        existing_idn = {c["identity_number"] for c in patients}
        if patient_identity_number in existing_idn:
            return [SlotSet("return_value", "already_exists")]

        new_patient = Patient(identity_number=patient_identity_number,
            first_name=patient_first_name,
            last_name=patient_last_name,
            age=patient_age)
        
        result = add_patient(new_patient)
        if result:
            return [SlotSet("return_value", "success")]
        else:
            return [SlotSet("return_value", "failed")]
