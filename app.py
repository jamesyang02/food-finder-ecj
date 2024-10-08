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

# TOP SECRET
@app.route("/nothingspecial")
def nothingspecial():
    return render_template("nothingspecial.html")

# Unused route
# test the API, loads on the home page
# Used to be used to verify during development, might still be useful
# acts as a "server up or down" test
@app.route("/api")
def test():
    return jsonify({
        "message": "Hello, World!"
    })

# submit a POST request to the Foodvisor API
# takes a JSON containing an image file and sends it to the Foodvisor API for analysis
# Attaches the required headers to allow the request to go through (CORS preflight OPTIONS check)
# this is really bulky and should be refactored to use a data URL, or ideally store on a server and send a URL
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
# takes a list of items in JSON format and asks for a recipe suggestion
# Data should have only one key "items" with a list of items as the value
@app.route("/api/groq", methods=["POST"])
def groq():
    client = Groq(
        api_key=os.environ.get("GROQ_SECRET_KEY"),
    )

    # get the list of items from the request
    item_list = request.json.get("items")
    if not item_list:
        return make_response("Couldn't find any food items, sorry!", 200)

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
    if chat_completion.choices[0]:
        return jsonify(chat_completion.choices[0].message.content)
    else:
        return make_response("No response from Groq", 200)

if __name__ == "__main__":
    app.run(debug=True, port=8080)