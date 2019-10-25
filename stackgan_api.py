import commands
import uuid
import json
import os
import argparse
import sys
import base64
from flask import Flask, request, jsonify, make_response
from werkzeug import secure_filename
sys.path.append(os.getcwd())

app = Flask(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="stackgan detect api")
    parser.add_argument("--model_path",
                        dest="model_path",
                        help="path to model load",
                        default=None,
                        type=str)
    args = parser.parse_args()
    return args


@app.route('/model_app/stackgan/detect', methods=['POST'])
def detect():
    uid = uuid.uuid1()
    # save file to Data/flowers/example_captions.txt
    print "start save txt"
    example_file = request.files["file"]
    filename = secure_filename(example_file.filename)
    base_path = os.path.dirname(__file__)
    caption_path = "Data/flowers/example_captions_%s" % uid
    example_file.save(os.path.join(base_path, caption_path))
    print "start txt transform"
    # transform  Data/flowers/example_captions.txt to Data/flowers/example_captions.t7
    s, o = commands.getstatusoutput("sh demo/flowers_demo.sh %s" % caption_path)
    if s != 0:
        # transfrom failed
        return o, 500
    # text to image
    print "start create img"
    s, o = commands.getstatusoutput("python demo/demo.py --model_path %s --uid %s" % (MODEL_PATH, uid))
    if s != 0:
        return o, 500
    # transform img to base64 code
    print "start img transform"
    response_data = {}
    response_data["type"] = "img"
    img_path = "Data/flowers/example_captions/sentence0_%s.jpg" % uid
    img = os.path.join(base_path, img_path)
    with open(img, "rb") as f:
        response_data["data"] = base64.b64encode(f.read())
    # return base64 code
    return json.dumps(response_data), 200
    

if __name__ == "__main__":
    args = parse_args()
    if args.model_path is None:
        print "model path is not set"
        sys.exit(1)
    else:
        MODEL_PATH = args.model_path
    app.run(host="0.0.0.0", port="80")
