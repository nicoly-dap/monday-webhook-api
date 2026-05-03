from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

MONDAY_TOKEN = os.environ.get("MONDAY_TOKEN")

def get_item_details(item_id):
    query = f"""
    {{
      items (ids: [{item_id}]) {{
        name
        column_values {{
          id
          type
          text
          value
        }}
      }}
    }}
    """
    response = requests.post(
        "https://api.monday.com/v2",
        headers={
            "Authorization": MONDAY_TOKEN,
            "Content-Type": "application/json"
        },
        json={"query": query}
    )
    return response.json()

@app.route('/api/monday-to-whatsapp', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return jsonify({"status": "active"}), 200

    if request.method == 'POST':
        try:
            data = request.json or {}

            if 'challenge' in data:
                return jsonify({"challenge": data['challenge']}), 200

            event = data.get('event', {})
            item_id = event.get('pulseId')

            if not item_id:
                return jsonify({"status": "ok"}), 200

            print(f"Novo item criado: {item_id}")

            details = get_item_details(item_id)
            print(f"Detalhes do item: {details}")

            items = details.get('data', {}).get('items', [])
            if not items:
                return jsonify({"status": "ok"}), 200

            item = items[0]
            item_name = item.get('name', '')
            columns = item.get('column_values', [])

            print(f"Todas as colunas: {columns}")

            whatsapp_number = None
            for col in columns:
                col_id = col.get('id', '').lower()
                col_text = col.get('text', '')
                if 'whatsapp' in col_id or 'phone' in col_id or 'telefone' in col_id:
                    whatsapp_number = col_text
                    break

            print(f"Cliente: {item_name} | WhatsApp: {whatsapp_number}")

            return jsonify({"status": "ok"}), 200

        except Exception as e:
            print(f"Erro: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Webhook running"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
