from typing import Any, Dict, List, Text
from datetime import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.services.patient_services import find_patient
from actions.services.appointment_services import get_appointments_by_patient
from actions.services.confirmation_services import get_config, send_sms, build_confirmation_message

class SendNotification(Action):
    def name(self) -> str:
        return "send_notification"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        patient_first_name = tracker.get_slot("send_notification_patient_first_name")
        patient_last_name = tracker.get_slot("send_notification_patient_last_name")
        appointment_idenity_number = None
        
        patient = find_patient(patient_first_name, patient_last_name, appointment_idenity_number)
        if patient is None:
            return [SlotSet("return_value", "send_notification_patient_not_found")]

        patient_appointments = get_appointments_by_patient(patient["id"])
        if patient_appointments == []:
            return [SlotSet("return_value", "appointment_not_found")]

        confirmation_message = build_confirmation_message(patient_first_name, patient_last_name, patient_appointments)

        config = get_config()
        sms_to = config["SMS_TO"]
        sms_from = config["SMS_FROM"]

        result = send_sms(sms_to, sms_from, confirmation_message)

        if result:
            return [SlotSet("return_value", "success")]
        else:
            return [SlotSet("return_value", "failed")]
