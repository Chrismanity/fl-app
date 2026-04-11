from flask import Flask, request, jsonify

app = Flask(__name__)

# One-time Lua payload
payload = ""

# One-time report from Roblox
report = {}

@app.route("/send", methods=["POST"])
def send():
    global payload
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "bad json"}), 400
    
    payload = data.get("AES", "")
    print("RECEIVED LUA:", payload)
    return jsonify({"status": "ok"})

@app.route("/get", methods=["GET"])
def get():
    global payload
    if payload == "":
        return jsonify({"AES": ""})
    
    temp = payload
    payload = ""  # one-time send
    return jsonify({"AES": temp})

@app.route("/report", methods=["POST"])
def report_post():
    global report
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "bad json"}), 400
    
    report = {
        "roblox_user": data.get("roblox_user", ""),
        "game_name": data.get("game_name", "")
    }
    print("REPORT:", report)
    return jsonify({"status": "ok"})

@app.route("/report", methods=["GET"])
def report_get():
    global report
    if not report:
        return jsonify({"roblox_user": "", "game_name": ""})
    
    temp = report
    report = {}  # clear after send
    return jsonify(temp)

if __name__ == "__main__":
    app.run()