from flask import Flask, jsonify, request, render_template, url_for, send_file
import useModel
import os
import urllib.parse
import base64
import datetime
import zipfile
from io import BytesIO

app = Flask(__name__)

saveString = []
saveResults = []
IMAGE_FOLDER = 'static'

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
    image = urllib.parse.unquote(image)
    image = image + "=" * ((4 - len(image) % 4) % 4)
    print(image)
    predict,result=useModel.useModelFromBase64(image)
    saveString.append(predict)
    saveResults.append(result)
    return jsonify(saveString[0]),200

@app.route('/saveDataset', methods=['POST'])
def saveDataset():
    saveString.clear()
    saveResults.clear()
    image=request.get_json()["name"]
    image = urllib.parse.unquote(image)
    image = image + "=" * ((4 - len(image) % 4) % 4)
    imageDate = datetime.datetime.now()
    imageName = "static/"+str(imageDate.strftime("%Y%m%d%M%S"))+".png"
    with open(imageName, "wb") as fh:
        fh.write(base64.urlsafe_b64decode(image))
    print(imageName+" saved")
    return jsonify(imageName+" saved"),200

@app.route('/showDataset', methods=['GET'])
def showDataset():
    files = os.listdir(IMAGE_FOLDER)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template('all-dataset.html', images=image_files)

@app.route('/download_all')
def download_all():
    # Create in-memory zip file
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zipf:
        for filename in os.listdir(IMAGE_FOLDER):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg', '.gif')):
                filepath = os.path.join(IMAGE_FOLDER, filename)
                zipf.write(filepath, arcname=filename)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='images.zip', mimetype='application/zip')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
