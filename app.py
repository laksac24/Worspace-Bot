from flask import Flask, request, jsonify
import datetime
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# import json
# import os

# google_creds = json.loads(os.environ["GOOGLE_CREDS"])
# creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("checkin sheet").sheet1

# Extract tasks and deadlines
def parse_tasks(message):
    task_lines = [line.strip() for line in message.split("\n") if "Task" in line]
    task_details = []
    deadlines = []
    for line in task_lines:
        task_details.append(line)
        match = re.search(r"\(.*?deadline:\s*(.*?)\)", line, re.IGNORECASE)
        if match:
            deadlines.append(match.group(1))
    return " | ".join(task_details), ", ".join(deadlines)

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    message = data["message"]["text"]
    name = data["user"]["displayName"]
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "check-in" in message.lower():
        msg_type = "Check-In"
    elif "check-out" in message.lower():
        msg_type = "Check-Out"
    else:
        return jsonify({"text": "Message not recognized as check-in or check-out."})

    tasks, deadlines = parse_tasks(message)
    sheet.append_row([name, time, msg_type, tasks, deadlines])

    return jsonify({"text": f"{msg_type} logged successfully for {name}!"})

if __name__ == "__main__":
    app.run(port=5000)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)