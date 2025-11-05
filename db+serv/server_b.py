from flask import Flask, jsonify
import psycopg2, json, pika, threading
app = Flask(__name__)


INDEX_FILE = "index.txt"

def connect():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="645258952Roma123",
        host="localhost",
        port=5432
    )

def send(data=None):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="answer")

    channel.basic_publish(exchange="", routing_key="answer", body=json.dumps(data))
    connection.close()

def get_index(filename):
    with open(filename) as f:
        return int(f.read())

def save_index(filename, index):
    with open(filename, "w") as f:
        f.write(str(index))

def worker():
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        all_data = json.loads(body)
        data = json.dumps(all_data["data"])

        index = all_data["params"].get("index")
        if index is not None:
            try:
                index = int(index)
            except (ValueError, TypeError):
                index = None

        method= all_data["method"]
        cur_id = get_index(INDEX_FILE)

        with connect() as conn:
            cur = conn.cursor()

            return_data =None

            if method == "GET":
                if index:
                    cur.execute("SELECT * FROM users WHERE id = %s;", (index,))
                else:
                    cur.execute("SELECT * FROM users;")

                rows = cur.fetchall()
                return_data = {row[0]: json.loads(row[1]) for row in rows}

            elif method == "POST":
                cur.execute(
                    "INSERT INTO users (id, file) VALUES (%s, %s);",
                    (cur_id, data)
                )
                save_index(INDEX_FILE, cur_id + 1)
                return_data = {"message": "added"}

            elif method == "DELETE":
                if index:
                    cur.execute("DELETE FROM users WHERE id = %s;", (index,))
                    cur.execute("UPDATE users SET id = id - 1 WHERE id > %s;", (index,))
                    save_index(INDEX_FILE, get_index(INDEX_FILE) - 1)
                else:
                    cur.execute("DELETE FROM users;")
                    save_index(INDEX_FILE, 1)
                return_data = {"message": f"Deleted id={index}" if index else "All records deleted"}

            elif method == "PATCH":
                if index:
                    cur.execute("UPDATE users SET file = %s WHERE id = %s;", (data, index))
                return_data = {"message": f"Updated id={index}" if index else "index not transferred to server"}

            conn.commit()

        send(return_data)



    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare("test")
    channel.basic_consume(queue="test", on_message_callback=callback, auto_ack=True)
    try:
        channel.start_consuming()
    except Exception as e:
        send({"message": str(e)})



@app.route("/create", methods=["GET"])
def create():
    try:
        conn = connect()
        curr = conn.cursor()
        curr.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id BIGINT PRIMARY KEY,
            file TEXT
        );
        """)
        conn.commit()
        conn.close()
        return jsonify({"message": "created"})
    except Exception as e:
        return jsonify({"message": str(e)})





if __name__ == "__main__":
    worker = threading.Thread(target=worker, daemon=True)
    worker.start()

    app.run(port=999, debug=True)