from flask import Flask, request, jsonify
import redis

app = Flask(__name__)

def connect():
    return redis.Redis(
        host = "localhost",
        port = 6379,
        db = 0
    )

def is_number(n):
    try:
        int(n)
        return True
    except:
        return False

def get_id():
    with open("id.txt") as f:
        return int(f.read())

def new_id(id):
    with open("id.txt", "w") as f:
        f.write(str(id))

@app.route("/send", methods=["POST"])
def send():
    index = request.args.get("index")
    data = request.data
    conn = connect()
    id = get_id()
    if not index:
        conn.set(f"{id}", data)
        new_id(id+1)
    else:
        if is_number(index):
            return jsonify({"message": "choose another index"})
        conn.set(index, data)

    return jsonify({"message": "sent"})

@app.route("/get", methods=["GET"])
def get_data():
    index = request.args.get("index")
    conn = connect()

    if index:
        value = conn.get(index)
    else:
        value = {}
        for key in conn.keys("*"):
            value[key.decode()] = conn.get(key).decode()

    conn.incr("got")

    if isinstance(value, dict):
        return value
    elif value:
        print(type(value))
        return value.decode()
    return str(value)

@app.route("/del", methods=["DELETE"])
def delete():
    index = request.args.get("index")
    conn = connect()
    conn.delete(index)

    return jsonify({"message": f"deleted index={index}"})

if __name__ == "__main__":
    app.run(port=9090, debug=True)