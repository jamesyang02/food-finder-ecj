from flask import Flask, request, jsonify, render_template, make_response
from flask_cors import CORS
from groq import Groq

import os
from dotenv import load_dotenv
load_dotenv()
import requests

app = Flask(__name__)
CORS(app)

# render the home page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/nothingspecial")
def nothingspecial():
    return render_template("nothingspecial.html")

# test the API, loads on the home page
# acts as a "server up or down" test
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

    headers = {
        "Authorization": "Api-Key " + SECRET_KEY,
        "Access-Control-Allow-Origin": "https://food-finder-ecj-next.vercel.app"
        }
    response = requests.post(url, headers=headers, files={"image": request.files.get("file")})
    if response.ok:
        data = response.json()
        print(data)
        return data
    else:
        return make_response(response.text, response.status_code)
    
# submit a POST request to Groq API
@app.route("/api/groq", methods=["POST"])
def groq():
    client = Groq(
        api_key=os.environ.get("GROQ_SECRET_KEY"),
    )

    # get the list of items from the request
    item_list = request.json["itemsList"]

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "I have a list of items: " + ", ".join(item_list) + ". Can you give one suggestion for a recipe?"
            }
        ],
        model="llama3-8b-8192",
    )
    print(chat_completion.choices[0].message.content)
    return jsonify(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    app.run(debug=True, port=8080)