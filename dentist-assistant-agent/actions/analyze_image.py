from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from actions.services.patient_services import find_patient 
from actions.services.image_analysis_services import analyze_image_with_llm

class AnalyzeImage(Action):
    def name(self) -> str:
        return "analyze_image"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        patient_first_name = tracker.get_slot("analyze_image_patient_first_name")
        patient_last_name = tracker.get_slot("analyze_image_patient_last_name")
        image_url = tracker.get_slot("analyze_image_image_url")
        image_analysis_instruction = tracker.get_slot("analyze_image_instruction")

        patient = find_patient(patient_first_name, patient_last_name, None)
        if patient is None:
            return [SlotSet("return_value", "patient_not_found")]

        image_analysis = analyze_image_with_llm(image_url, image_analysis_instruction)

        print("Image analysis result:", image_analysis)

        dispatcher.utter_message(
            response="utter_image_analysis_report",
            image_analysis=image_analysis
        )
            
        if image_analysis is not None:
            return [SlotSet("return_value", "success")]
        else:
            return [SlotSet("return_value", "failed")]
