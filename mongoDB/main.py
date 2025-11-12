from flask import Flask, request, jsonify, Response
import pymongo, requests,json


url ="mongodb+srv://Roma:645258952Roma123@test.hv0s3xa.mongodb.net/?appName=test"

app = Flask(__name__)


def connect():
    return pymongo.MongoClient(url)

@app.route("/send", methods=["POST"])
def send():
    conn = connect()
    db = conn["test"]

    user_col = db["users"]

    x = list(user_col.find({}, { "_id": 0}))
    for el in x:
        if "_id" in el:
            el["_id"] = str(el["_id"])

    return jsonify({i+1: el for i, el in enumerate(x)})


if __name__ == "__main__":
    app.run(port=777, debug=True)


