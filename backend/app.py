from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- add this!

app = Flask(__name__)
CORS(app)  # <-- add this!

@app.route('/', methods=['GET'])
def home():
    return "Nurturing Young Brains Flask Server Running!"

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"message": "Data received successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)