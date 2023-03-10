import httpx
import json
from my_app.schemas import Activity

url = 'https://www.boredapi.com/api/activity'


def get_my_activity() -> str:
    client = httpx.Client()
    response = client.get(url)
    response_json = json.loads(response.text)
    activity_obj = Activity.parse_obj(response_json)
    return activity_obj


