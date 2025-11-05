from flask import Flask, request, jsonify
import pika, json, threading, requests
from datetime import datetime

ANSWER = "answer.json"
app = Flask(__name__)


def worker():
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        data = json.loads(body)
        with open(ANSWER, "w", encoding="utf-8") as file:
            now = datetime.now().isoformat()
            json.dump({now: data}, file, indent=2)

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare("answer")
    channel.basic_consume(queue="answer", on_message_callback=callback, auto_ack=True)
    try:
        channel.start_consuming()
    except Exception as e:
        pass

def send(method, params=None, data=None):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="test")

    message = {
        "method": method,
        "params": params,
        "data": data
    }

    channel.basic_publish(exchange="", routing_key="test", body=json.dumps(message))
    print(f" [x] Sent {message}")
    connection.close()



@app.route("/user", methods=["GET", "POST", "DELETE", "PATCH"])
def response():
    try:
        params = request.args.to_dict()
        method = request.method
        json_data = request.get_json(silent=True)

        send(method, params, json_data)

        return jsonify({"message": "sent"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/create", methods=["GET"])
def create():
    try:
        answer = requests.get("http://127.0.0.1:999/create")

        return jsonify(answer.json()), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    worker_thread = threading.Thread(target=worker, daemon=True)
    worker_thread.start()

    app.run(port=998, debug=True)
