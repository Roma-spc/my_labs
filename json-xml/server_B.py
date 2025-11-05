from flask import Flask, request, jsonify, Response
import uuid
import xml.etree.ElementTree as ET
import xmltodict

def parse_json(data):
    root = ET.Element("data")

    ET.SubElement(root, "id").text = data["id"]

    personal_data = ET.SubElement(root, "personal_data")
    ET.SubElement(personal_data, "name").text = data["personal_data"]["name"]
    ET.SubElement(personal_data, "surname").text = data["personal_data"]["surname"]
    ET.SubElement(personal_data, "age").text = data["personal_data"]["age"]

    address = ET.SubElement(root, "address")
    ET.SubElement(address, "street").text = data["address"]["street"]
    ET.SubElement(address, "number").text = data["address"]["number"]

    work_place = ET.SubElement(root, "work_place")
    ET.SubElement(work_place, "name").text = data["work_place"]["name"]
    ET.SubElement(work_place, "position").text = data["work_place"]["position"]
    ET.SubElement(work_place, "company").text = data["work_place"]["company"]

    return root
app = Flask(__name__)

@app.route("/get_json", methods=["POST"])
def send_xml():
    try:
        data = request.get_json()
        unique_id = request.args.get("id") or str(uuid.uuid4())
        data["id"] = unique_id

        root = parse_json(data)
        xml_str = ET.tostring(root, encoding='utf-8')
        return Response(xml_str, mimetype='application/xml')

    except Exception as e:
        return Response("Invalid JSON", status=500)


@app.route("/get_xml", methods=["POST"])
def send_json():
    try:
        data = request.data
        root = ET.fromstring(data)
        unique_id = request.args.get("id") or str(uuid.uuid4())

        ET.SubElement(root, "id").text = unique_id
        str_xml = ET.tostring(root, encoding="utf-8")

        formatted = xmltodict.parse(str_xml)

        formatted = formatted["data"]

        return jsonify(formatted), 200

    except Exception as e:
        return Response(f"Invalid JSON: {e}", status=500)


if __name__ == "__main__":
    app.run(port=6001, debug=True)