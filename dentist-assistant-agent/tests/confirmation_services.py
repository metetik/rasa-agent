from actions.services.confirmation_services import send_sms, get_config
try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

app_config = get_config()

def test_send_sms():
	sms_to = app_config["SMS_TO"]
	sms_from = app_config["SMS_FROM"]
	sms_content = "Hello, this is a test message"

	assert send_sms(sms_to, sms_from, sms_content)
