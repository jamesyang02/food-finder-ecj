from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS

import os
from dotenv import load_dotenv
load_dotenv()
import requests

app = Flask(__name__)
CORS(app)

# render the home page file
@app.route("/")
def index():
    return render_template("./app/page.tsx")

# test the API
@app.route("/api")
def test():
    return jsonify({
        "message": "Hello, World!"
    })

# submit a POST request to the Foodvisor API
@app.route("/api/analyze", methods=["POST"])
def analyze():
    SECRET_KEY = os.getenv("FOODVISOR_SECRET_KEY")
    url = "https://vision.foodvisor.io/api/1.0/en/analysis/"

    headers = {"Authorization": "Api-Key " + SECRET_KEY}
    response = requests.post(url, headers=headers, files={"image": request.files.get("file")})
    if response.ok:
        data = response.json()
        print(data)
        return data
    else:
        return make_response(response.text, response.status_code)

if __name__ == "__main__":
    app.run(debug=True, port=8080)