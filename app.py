from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    
    _, ycrcb_encoded = cv2.imencode('.png', ycrcb)
    _, hsv_encoded = cv2.imencode('.png', hsv)
    _, lab_encoded = cv2.imencode('.png', lab)

    ycrcb_b64 = base64.b64encode(ycrcb_encoded).decode('utf-8')
    hsv_b64 = base64.b64encode(hsv_encoded).decode('utf-8')
    lab_b64 = base64.b64encode(lab_encoded).decode('utf-8')

    return jsonify({'ycrcb': ycrcb_b64, 'hsv': hsv_b64, 'lab': lab_b64})

if __name__ == '__main__':
    app.run(debug=True)