from flask import Flask, request, jsonify

app = Flask(__name__)

# Existing globals
payload = ""
report = {}

# New: Conversion system globals
conversion_requests = {}
conversion_results = {}

# ==========================================
# EXISTING ENDPOINTS
# ==========================================

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

# ==========================================
# NEW: CONVERSION ENDPOINTS
# ==========================================

@app.route("/convert/request", methods=["POST"])
def convert_request_post():
    """Roblox sends unconverted script here"""
    global conversion_requests
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "bad json"}), 400
    
    script = data.get("script", "")
    auto_convert = data.get("autoConvert", True)
    request_id = data.get("requestId", "")
    
    conversion_requests["latest"] = {
        "script": script,
        "autoConvert": auto_convert,
        "requestId": request_id
    }
    
    print(f"[CONVERT REQUEST] ID: {request_id}, Length: {len(script)} chars")
    return jsonify({"status": "ok"})

@app.route("/convert/request", methods=["GET"])
def convert_request_get():
    """C# app polls this to get scripts to convert"""
    global conversion_requests
    latest = conversion_requests.get("latest", {})
    return jsonify(latest)

@app.route("/convert/response", methods=["POST"])
def convert_response_post():
    """C# app sends converted script here"""
    global conversion_results
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "bad json"}), 400
    
    request_id = data.get("requestId", "")
    converted = data.get("converted", "")
    
    conversion_results[request_id] = converted
    print(f"[CONVERT RESPONSE] ID: {request_id}, Length: {len(converted)} chars")
    return jsonify({"status": "ok"})

@app.route("/convert/response", methods=["GET"])
def convert_response_get():
    """Roblox polls this to get the converted script"""
    global conversion_results
    request_id = request.args.get("id", "")
    
    if request_id in conversion_results:
        converted = conversion_results[request_id]
        del conversion_results[request_id]  # Clean up after sending
        print(f"[CONVERT SENT] ID: {request_id}")
        return jsonify({"converted": converted})
    else:
        return jsonify({}), 404

# ==========================================
# RUN SERVER
# ==========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
