try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

import os
import json
from twilio.rest import Client
from actions.services.staff_services import get_dentist_by_id


def get_config():
    with open("/workspaces/rasa-agent/dentist-assistant-agent/app_config.toml", "rb") as f:
        config = tomllib.load(f)

    return config

config = get_config()

def build_confirmation_message(patient_first_name, patient_last_name, patient_appointments):
    message_content = ""

    message_content = f"Hello {patient_first_name} {patient_last_name},\n\n"
    message_content += "Here are your upcoming appointments:\n"
    for appointment in patient_appointments:
        dentist_id = appointment["dentist_id"]
        dentist_obj = get_dentist_by_id(dentist_id)
        dentist_first_name = dentist_obj["first_name"]
        dentist_last_name = dentist_obj["last_name"]

        start_date = appointment["start_date"]
        end_date = f" - {appointment['end_date']}" if appointment["end_date"] is not None else ""

        message_content += f"- At {start_date}{end_date} with Dt. {dentist_first_name} {dentist_last_name} .\n"

    message_content += "\nIf you have any questions about your appointments, please contact us."

    return message_content

def send_sms(sms_to, sms_from, sms_content):
    account_sid = config["TWILIO_SID"]
    auth_token = config["TWILIO_TOKEN"]

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=sms_content,
        from_=sms_from,
        to=sms_to,
    )
    print(f"SMS sent to {sms_to} from {sms_from}: \n{sms_content}")

    return message.error_code is None

def send_email(email_to, email_subject, email_content):
    return True