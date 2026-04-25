from flask import Flask, request, jsonify

app = Flask(__name__)

payload = ""

@app.route("/send", methods=["POST"])
def send():
    global payload
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "bad json"}), 400
    
    payload = data.get("AES", "")
    print("RECEIVED:", payload)
    return jsonify({"status": "ok"})

@app.route("/get", methods=["GET"])
def get():
    global payload
    if payload == "":
        return jsonify({"AES": ""})
    
    temp = payload
    payload = ""
    return jsonify({"AES": temp})

if __name__ == "__main__":
    app.run()
