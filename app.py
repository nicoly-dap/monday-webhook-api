from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/monday-to-whatsapp', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return jsonify({"status": "active", "message": "Webhook is running"}), 200
    
    if request.method == 'POST':
        try:
            data = request.json
            print(f"Data received: {data}")
            return jsonify({"status": "received", "data": data}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Webhook API running"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
