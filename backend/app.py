from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os  # <-- important for paths

app = Flask(__name__)
CORS(app)

# Make sure the backend/model or backend/data folder exists
SAVE_FOLDER = 'backend/model'
SAVE_FILE = os.path.join(SAVE_FOLDER, 'comments.json')

@app.route('/', methods=['GET'])
def home():
    return "Nurturing Young Brains Flask Server Running!"

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    print("Received data:", data)

    # Save the data into a JSON file
    try:
        if not os.path.exists(SAVE_FOLDER):
            os.makedirs(SAVE_FOLDER)  # create the folder if it doesn't exist

        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("Data saved to", SAVE_FILE)

    except Exception as e:
        print("Error saving data:", e)
        return jsonify({"message": "Error saving data!"}), 500

    return jsonify({"message": "Data received and saved successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)