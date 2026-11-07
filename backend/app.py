from flask import Flask, jsonify, request
from flask_cors import CORS
from database import get_connection

app=Flask(__name__)
CORS(app,resources={
    r"/api/*": {"origins": ["http://127.0.0.1:5500", "https://brave-bay-03c962010.5.azurestaticapps.net"]}
})

@app.get("/api/fact")
def get_fact():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT TOP (1) fact FROM ProgrammingFacts ORDER BY NEWID()"
            )
            row = cursor.fetchone()
    if row is None:
        return jsonify({"error": "No facrs found."}), 404
    return jsonify({"fact": row[0]})

@app.post("/api/study")
def study():
    data=request.get_json()
    topic= data.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "Please enter what you are learning."}),400
    return jsonify({"message": "Studying " +topic+ " will pay off in the future, keep going!"})