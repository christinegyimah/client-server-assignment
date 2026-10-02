from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app=Flask(__name__)
CORS(app,resources={
    r"/api/*": {"origins": ["http://127.0.0.1:5500", "https://brave-bay-03c962010.5.azurestaticapps.net"]}
})
facts=["Programming uses 0’s and 1’s because computers operate on binary code, a base-2 numeral system. "
    "This system works because digital electronics, like transistors, have two states: on (1) and off (0). Binary forms the foundation of all computer operations.",
    "JavaScript was created in just 10 days by Brendan Eich in 1995. Despite its name, it has no real relation to Java.",
    "The C language was so influential that it led to the creation of both Python and JavaScript, along with many other languages.",
    "There is a programming language called “LOLCODE” designed to look like lolcats memes.",
    "The most lines of code ever written for a single project is considered to be in Google’s repository, which held over 2 billion lines as of 2015."]
@app.get("/api/fact")
def get_fact():
    return jsonify({"fact": random.choice(facts)})

@app.post("/api/study")
def study():
    data=request.get_json()
    topic= data.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Please enter what you are learning."}),400
    return jsonify({"message": "Studying " +topic+ " will pay off in the future, keep going!"})