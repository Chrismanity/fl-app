from flask import Flask, request, jsonify

app = Flask(__name__)

payload = ""
report = {}

@app.route("/send", methods=["POST"])
def send():
    global payload
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "bad json"}), 400
    
    payload = data.get("AES", "")
    print(f"RECEIVED: {payload}")
    return jsonify({"status": "ok"})

@app.route("/get", methods=["GET"])
def get():
    global payload
    if payload == "":
        return jsonify({"AES": ""})
    
    temp = payload
    payload = ""
    print(f"SENT TO CLIENT: {temp}")
    return jsonify({"AES": temp})

@app.route("/report", methods=["POST"])
def report_post():
    global report
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "bad json"}), 400
    
    report = {"roblox_user": data.get("roblox_user", "")}
    print(f"REPORT: {report}")
    return jsonify({"status": "ok"})

@app.route("/report", methods=["GET"])
def report_get():
    global report
    if not report:
        return jsonify({"roblox_user": ""})
    
    temp = report
    report = {}
    return jsonify(temp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
