from flask import Flask, jsonify, request, render_template, url_for
import useModel
import os
import urllib.parse
import base64

app = Flask(__name__)

saveString = []
saveResults = []

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route('/processTest')
def get_incomes():
    return render_template("process-result.html",description = saveResults)

@app.route('/process', methods=['POST'])
def add_income():
    saveString.clear()
    saveResults.clear()
    image=request.get_json()["name"]
    image = image + '=' * (4 - len(image) % 4)
    predict,result=useModel.useModelFromBase64(image)
    saveString.append(predict)
    saveResults.append(result)
    return jsonify(saveString[0]),200


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
