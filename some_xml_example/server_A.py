from flask import Flask, jsonify, Response, request
import requests

app = Flask(__name__)


SERVER_B = "http://127.0.0.1:1010"

@app.route("/parse_json", methods=["POST"])
def parse_json():
    data = request.get_json()
    answer = requests.post(f"{SERVER_B}/send_xml", json=data)
    return Response(answer.content, mimetype="application/xml", status=200)

@app.route("/parse_xml", methods=["POST"])
def parse_xml():
    data = request.data.decode("utf-8")
    answer = requests.post(f"{SERVER_B}/send_json", data=data)
    return jsonify(answer.json()), 200


if __name__ == "__main__":
    app.run(port=1011, debug=True)

