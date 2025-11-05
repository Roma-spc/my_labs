from flask import Flask, request, jsonify
import sqlite3, json, pika, threading, requests
app = Flask(__name__)

def worker():
    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            data["name"] = data["name"] + " " + data["surname"]
            del data["surname"]

            json_str = json.dumps(data)

            db = sqlite3.connect("database.db")
            cursor = db.cursor()
            cursor.execute("INSERT INTO files (data) VALUES (?)", (json_str,))
            db.commit()
            db.close()

            requests.post("http://127.0.0.1:5002/status", json={"successfully": "yes"})
        except:
            requests.post("http://127.0.0.1:5002/status", json={"successfully": "no"})

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="responses")
    channel.basic_consume(queue="responses", on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

@app.route("/answer", methods=["POST"])
def answer():
    try:
        data = request.get_json()

        if data["successfully"] == "yes":
            return jsonify(data), 200
        return jsonify(data), 500
    except:
        return jsonify({"successfully": "no"}), 500


@app.route("/get", methods=["GET"])
def get_jsons():
    try:
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM files")
        rows = cursor.fetchall()
        db.close()

        result = {str(row[0]): json.loads(row[1]) for row in rows}
        return jsonify(result), 200
    except:
        return jsonify("Can't show the database"), 500



@app.route("/get/<int:index>", methods=["GET"])
def get_json(index):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM files WHERE id = ?",(index,))
    rows = cursor.fetchone()
    db.close()
    try:
        result = {str(rows[0]): json.loads(rows[1])}
        return jsonify(result), 200
    except TypeError:
        return jsonify("Index out of range"), 500

if __name__ == "__main__":
    worker = threading.Thread(target=worker, daemon=True)
    worker.start()

    app.run(port=5003, debug=True)