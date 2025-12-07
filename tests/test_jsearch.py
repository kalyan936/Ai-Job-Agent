import os
import requests

url = "https://jsearch.p.rapidapi.com/search"

headers = {
    "X-RapidAPI-Key": os.environ["JSEARCH_API_KEY"],
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

params = {
    "query": "AI Engineer in India",
    "page": "1",
    "num_pages": "1"
}

res = requests.get(url, headers=headers, params=params)
print(res.status_code)
print(res.json())
