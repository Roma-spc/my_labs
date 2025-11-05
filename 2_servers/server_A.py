from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json()
        data["time"] = datetime.now().isoformat()
        response = requests.post("http://127.0.0.1:5001/send", json=data)

        return jsonify(response.json()), 200
    except:
        return jsonify("Виникла помилка"), 500

@app.route("/jsons", methods=["GET"])
def jsons():
    try:
        response = requests.get("http://127.0.0.1:5001/get")
        data = response.json()
        return jsonify(data), 200
    except:
        return jsonify("Виникла помилка"), 500

@app.route("/jsons/<int:index>", methods=["GET"])
def json(index):
    try:
        response = requests.get(f"http://127.0.0.1:5001/get/{index}")
        data = response.json()
        return jsonify(data), 200
    except:
        return jsonify("Виникла помилка"), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)