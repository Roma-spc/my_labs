from flask import Flask, request, jsonify
import requests, pika, json
from datetime import datetime

app = Flask(__name__)


def send_to_queue(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='responses')

    channel.basic_publish(exchange="", routing_key="responses", body=json.dumps(data))
    connection.close()
@app.route("/send", methods=["POST"])
def send():
    try:
        data = request.get_json()
        data["time"] = datetime.now().isoformat()
        send_to_queue(data)
        return jsonify({"status": "accepted"}), 200
    except:
        return jsonify({"status": "rejected"}), 500

@app.route("/status", methods=["POST"])
def send_status():
    try:
        with open('status.json', 'w') as f:
            now = datetime.now().isoformat()
            json.dump({now: request.get_json()}, f)
        return jsonify({"written": "yes"}), 200
    except:
        return jsonify({"written": "no"}), 500

@app.route("/jsons", methods=["GET"])
def get_jsons():
    try:
        response = requests.get("http://127.0.0.1:5003/get")
        data = response.json()
        return jsonify(data), 200
    except:
        return jsonify("Виникла помилка"), 500

@app.route("/jsons/<int:index>", methods=["GET"])
def get_json(index):
    try:
        response = requests.get(f"http://127.0.0.1:5003/get/{index}")
        data = response.json()
        return jsonify(data), 200
    except:
        return jsonify("Виникла помилка"), 500


if __name__ == "__main__":
    app.run(port=5002, debug=True)