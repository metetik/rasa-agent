import os

from datetime import datetime
from typing import List, Optional
from rasa.shared.nlu.training_data.message import Message
# from actions.entity_extractor import duckling_entity_extractor
# from dotenv import load_dotenv
from rasa.nlu.extractors.duckling_entity_extractor import DucklingEntityExtractor

# load_dotenv()
duckling_url = os.environ.get("RASA_DUCKLING_HTTP_URL")

duckling_config = {
    **DucklingEntityExtractor.get_default_config(),
    "url": duckling_url,
    "dimensions": ["time"]
}

duckling_entity_extractor = DucklingEntityExtractor(duckling_config)

def parse_datetime(text: str) -> Optional[datetime]:
    # If the text is already a date slot value extracted from Duckling,
    # we can just use it
    try:
        result = datetime.fromisoformat(text)
        return result.replace(tzinfo=None)
    except ValueError:
        pass

    # Otherwise, we need to parse the value set by the LLM
    # using Duckling
    msg = Message.build(text)
    duckling_entity_extractor.process([msg])
    if len(msg.data.get("entities", [])) == 0:
        return None

    parsed_value = msg.data["entities"][0]["value"]
    if isinstance(parsed_value, dict):
        parsed_value = parsed_value["from"]

    result = datetime.fromisoformat(parsed_value)
    return result.replace(tzinfo=None)
