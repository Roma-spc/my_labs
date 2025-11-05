from flask import Flask, request, jsonify
import sqlite3, json
app = Flask(__name__)

@app.route("/send", methods=["POST"])
def reformate():
    try:
        data = request.get_json()
        data["name"] = data["name"] + " " + data["surname"]
        del data["surname"]

        json_str = json.dumps(data)

        db = sqlite3.connect("mydb.db")
        cursor = db.cursor()
        cursor.execute("INSERT INTO files (data) VALUES (?)", (json_str,))
        db.commit()
        db.close()
        return jsonify({"successfully": "yes"}), 200
    except:
        return jsonify({"successfully": "no"}), 500


@app.route("/get", methods=["GET"])
def get_jsons():
    try:
        db = sqlite3.connect("mydb.db")
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
    db = sqlite3.connect("mydb.db")
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
    app.run(port=5001, debug=True)