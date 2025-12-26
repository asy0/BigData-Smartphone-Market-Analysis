from dotenv import load_dotenv
import os

# Load .env on import
load_dotenv()
# Search for a device
import requests

def search_device(device_name):
    url = "https://api.mobileapi.dev/devices/search/"
    params = {
        "name": device_name,
        "key": os.getenv("MOBILEAPIKEY")
    }
    response = requests.get(url, params=params)
    return response.json()

# Usage
result = search_device("iPhone 17 Pro")
print(result)