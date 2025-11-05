from xml.etree.ElementTree import SubElement

from flask import Flask, request, jsonify, Response
import requests
import uuid

app = Flask(__name__)

@app.route("/json/<string:some_string>", methods=["POST"])
def send_json(some_string):
    try:
        data = request.get_json()
        some_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, some_string))
        response = requests.post("http://127.0.0.1:6001/get_json", json=data, params={"id": some_id})
        return Response(response.content, mimetype="application/xml", status=200)
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@app.route("/xml/<string:some_string>", methods=["POST"])
def send_xml(some_string):
    try:
        data = request.data.decode("utf-8")
        some_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, some_string))

        response = requests.post("http://127.0.0.1:6001/get_xml", data=data, params={"id": some_id})

        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500



if __name__ == "__main__":
    app.run(port=6000, debug=True)