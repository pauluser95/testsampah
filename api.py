from flask import Flask, jsonify, request, redirect, url_for
import useModel
import os

app = Flask(__name__)

saveString = []

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route('/processTest')
def get_incomes():
    return jsonify(saveString)

@app.route('/process', methods=['POST'])
def add_income():
    saveString.clear()
    print(request.get_json())
    image=request.get_json()["name"]
    print(image)
    saveString.append(useModel.useModelFromBase64(image))
    return jsonify(saveString[0]),200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
