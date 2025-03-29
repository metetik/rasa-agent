import base64
import requests
from openai import OpenAI

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

def get_config():
    with open("/workspaces/rasa-agent/dentist-assistant-agent/app_config.toml", "rb") as f:
        config = tomllib.load(f)

    return config

config = get_config()

XAI_API_KEY = config["XAI_API_KEY"]

def encode_image_from_url(image_url):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status() 

        image_data = response.content
        encoded_string = base64.b64encode(image_data).decode("utf-8")
        return encoded_string

    except requests.exceptions.RequestException as e:
        print(f"Error: An error occurred while getting the image from the URL: {e}")
        return None

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

def analyze_image_with_llm(image_url, prompt):
	base64_image  = encode_image_from_url(image_url)

	if base64_image is None:
		return None
	
	system_prompt = """You are an AI assistant specialized in dentistry. Your purpose is to assist dentists and dental professionals by analyzing dental images, such as panoramic X-rays, intraoral photos, or other tooth-related visuals. You will receive a base64-encoded image along with a user request (e.g., "Does this tooth have a cavity?" or "Provide a general analysis of the X-ray"). Your responsibilities include:

	1. **Image Analysis**: Examine the dental image to identify key features such as tooth positions (using standard dental numbering), jaw anatomy, bone structure, and any visible abnormalities (e.g., cavities, fractures, fillings, root issues, cysts, or tumors).
	2. **Professional Terminology**: Use accurate dental terms (e.g., "mesial," "distal," "occlusal," "periapical") to describe findings clearly and precisely.
	3. **Tailored Response**: Adapt your analysis to the user’s specific request. For a general query, provide a comprehensive summary of observations; for a specific question (e.g., "Is there decay in tooth 32?"), focus solely on the requested area.
	4. **Limitations**: Do not provide a medical diagnosis. Frame your observations as "potential" or "noted" findings and stress that a qualified dentist must confirm the results.
	5. **Response Structure**: Organize your output as follows:
	- **General Findings**: A concise overview of the image’s key elements.
	- **Detailed Analysis**: In-depth insights based on the user’s request.
	- **Recommendation**: Practical next steps for the dentist (e.g., "Further clinical evaluation suggested").
	6. **Error Handling**: If the image is unclear, low-quality, or unsuitable (e.g., not a dental image), inform the user politely and request a better or relevant image.

	You are provided with the image in base64 format and the user’s prompt. Deliver an accurate, professional, and supportive analysis to meet the user’s needs effectively."""
	
	messages = [
		{
			"role": "system", 
			"content": system_prompt
		},
		{
			"role": "user",
			"content": [
				{
					"type": "image_url",
					"image_url": {
						"url": f"data:image/jpeg;base64,{base64_image}",
						"detail": "high",
					},
				},
				{
					"type": "text",
					"text": prompt,
				},
			],
		},
	]

	completion = client.chat.completions.create(
		model="grok-2-vision-latest",
		messages=messages,
		temperature=0.01,
	)

	return completion.choices[0].message.content