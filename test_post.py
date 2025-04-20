import requests

url = "http://127.0.0.1:5000/"
headers = {
    "Content-Type": "application/json"
}

data = {
    "message": {
        "text": "Check-In\nTask: Finish article draft (deadline: 5pm)"
    },
    "user": {
        "displayName": "Oscar"
    }
}

response = requests.post(url, json=data, headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.json())
