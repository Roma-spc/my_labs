from flask import Flask, jsonify, request, Response
import json, xmltodict, requests, psycopg2

app = Flask(__name__)

def get_id(filename):
    with open(filename) as f:
        return int(f.read())

def save_id(filename, id):
    with open(filename, "w") as f:
        f.write(str(id))

def connection():
    return psycopg2.connect(
        dbname= "postgres",
        user = "postgres",
        password="645258952Roma123",
        host="localhost",
        port=5432
    )

@app.route("/send_xml", methods=["POST"])
def dict_to_xml():
    json_file = request.get_json()
    xml_str = xmltodict.unparse(json_file, pretty=True)

    with connection() as conn:
        cur = conn.cursor()
        id = get_id("id_xml.txt")
        cur.execute("INSERT INTO xmls (id, file) VALUES (%s, %s)", (id, xml_str))
        save_id("id_xml.txt", id+1)
        conn.commit()

    return Response(xml_str, mimetype="application/xml", status=200)


@app.route("/send_json", methods=["POST"])
def xml_to_dict():
    xml_str = request.data
    json_file = xmltodict.parse(xml_str)
    json_str = json.dumps(json_file)

    with connection() as conn:
        cur = conn.cursor()
        id = get_id("id_json.txt")
        cur.execute("INSERT INTO jsons (id, file) VALUES (%s, %s)", (id, json_str))
        save_id("id_json.txt", id+1)
        conn.commit()

    return jsonify(json_file), 200


if __name__ == "__main__":
    app.run(port=1010, debug=True)