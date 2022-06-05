import json
from flask import request
from chatbot import app


@app.route("/", methods=["GET", "POST"])
def index():
    req = request.json
    response = {"response": {
        "text": "",
        "tts": "",
        "end_session": False
    },
        "session": req["session"],
        "version": req["version"]}
    if "кыр сосичка" in req["request"]["command"].lower() and "вездекод" in req["request"]["command"].lower():
        response["response"]["text"] = "Привет вездекодерам!"
        response["response"]["tts"] = "Привет вездекодерам!"
    return json.dumps(response)
