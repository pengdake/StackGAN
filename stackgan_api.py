import commands
import json
import os
import sys
sys.path.append(os.getcwd())
import base64
from flask import Flask, request
from werkzeug import secure_filename
from demo.demo import text_to_image



app = Flask(__name__)


@app.route('/detect', methods=['POST'])
def detect():
    # save file to Data/flowers/example_captions.txt
    example_file = request.files["file"]
    filename = secure_filename(example_file.filename)
    base_path = os.path.dirname(__file__)
    example_file.save(os.path.join(base_path, "Data/flowers/example_captions.txt"))
    # transform  Data/flowers/example_captions.txt to Data/flowers/example_captions.t7
    s, o = commands.getstatusoutput("sh demo/flowers_demo.sh")
    if s != 0:
        # transfrom failed
        return o, 500
    # text to image
    text_to_image()
    # transform img to base64 code
    response_data = {}
    response_data["type"] = "img"
    img = os.path.join(base_path, "Data/flowers/example_captions/sentence0.jpg")
    with open(img, "rb") as f:
        response_data["data"] = base64.b64encode(f.read())
    # return base64 code
    return json.dumps(response_data), 200
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="9000")
