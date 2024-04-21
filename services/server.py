import requests
import json

# URL вашего Flask-приложения
base_url = "http://127.0.0.1:5000"

# Данные для запроса /stations/detailed
data_detailed = {
    "stationName": "Комсомольская",
    "time": "1985-09-25 17:45:30.005"
}

def post_ans(data: dict):
    data_detailed["stationName"] = data["station"]
    time_text = str(data["year"]) + '-' + str(data["month"]) + '-' + str(data["day"]) + \
    '18:00:00'
    data_detailed["time"] = time_text
    response_detailed = requests.post(f"{base_url}/stations/detailed", json=data_detailed)
    print("Response from /stations/detailed:")
    print(json.dumps(response_detailed.json(), indent=4,ensure_ascii=False))