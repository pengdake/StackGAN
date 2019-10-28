import commands
import uuid
import os
import argparse
import sys
import base64
from flask import Flask, request, jsonify, make_response
from werkzeug.contrib.cache import SimpleCache
sys.path.append(os.getcwd())

cache = SimpleCache()
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


@app.route('/detect', methods=['POST'])
def detect():
    if cache.get("detecting") == "true":
        return make_response("server is busy, try again later", 400)
    cache.set("detecting", "true")
    uid = uuid.uuid1()
    # save file to Data/flowers/example_captions.txt
    example_file = request.files.get("file")
    if not example_file:
        cache.set("detecting", "false")
        return make_response("Please provide file for detect", 400)
    base_path = os.path.abspath(os.getcwd())
    caption_path = "%s/Data/flowers/example_captions_%s.txt" % (base_path, uid)
    example_file.save(caption_path)
    # transform  Data/flowers/example_captions.txt to Data/flowers/example_captions.t7
    s, o = commands.getstatusoutput("sh %s/demo/flowers_demo.sh %s" % (base_path, caption_path.split(".")[0]))
    if s != 0:
        # transfrom failed
        cache.set("detecting", "false")
        return make_response(o, 400)
    # text to image
    s, o = commands.getstatusoutput("cd %s && python demo/demo.py --model_path %s --uid %s" % (base_path, MODEL_PATH, uid))
    cache.set("detecting", "false")
    if s != 0:
        return make_response(o, 400)
    # transform img to base64 code
    response_data = {"type": "img"}
    img_path = "%s/Data/flowers/example_captions_%s/sentence0.jpg" % (base_path, uid)
    with open(img_path, "rb") as f:
        response_data["data"] = "data:image/jpg;base64,%s" % base64.b64encode(f.read())
    return make_response(jsonify(response_data), 200)
    

if __name__ == "__main__":
    args = parse_args()
    if args.model_path is None:
        print "model path is not set"
        sys.exit(1)
    else:
        MODEL_PATH = args.model_path + "/model.ckpt"
    cache.set("detecting", "false")
    app.run(host="0.0.0.0", port="80")
