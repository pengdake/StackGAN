import commands
import uuid
import json
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
    if cache.get("training") == "true":
        return make_response("server is busy, train again later", 400)
    cache.set("training", "true")
    uid = uuid.uuid1()
    # save file to Data/flowers/example_captions.txt
    print "start save txt"
    example_file = request.files["file"]
    base_path = os.path.dirname(os.path.dirname(__file__))
    base_path = os.path.abspath(os.getcwd())
    caption_path = "%s/Data/flowers/example_captions_%s.txt" % (base_path, uid)
    example_file.save(caption_path)
    print "start txt transform"
    # transform  Data/flowers/example_captions.txt to Data/flowers/example_captions.t7
    s, o = commands.getstatusoutput("sh %s/demo/flowers_demo.sh %s" % (base_path, caption_path.split(".")[0]))
    if s != 0:
        # transfrom failed
        return make_response(o, 400)
    # text to image
    print "start create img"
    s, o = commands.getstatusoutput("python %s/demo/demo.py --model_path %s --uid %s" % (base_path, MODEL_PATH, uid))
    if s != 0:
        return make_response(o, 400)
    cache.set("training", "false")
    # transform img to base64 code
    print "start img transform"
    response_data = {}
    response_data["type"] = "img"
    img_path = "%s/Data/flowers/example_captions_%s/sentence0.jpg" % (base_path, uid)
    with open(img_path, "rb") as f:
        response_data["data"] = "data:image/jpg;base64,%s" % base64.b64encode(f.read())
    # return base64 code
    return make_response(jsonify(response_data), 200)
    

if __name__ == "__main__":
    args = parse_args()
    if args.model_path is None:
        print "model path is not set"
        sys.exit(1)
    else:
        MODEL_PATH = args.model_path + "/model.ckpt"
    cache.set("training", "false")
    app.run(host="0.0.0.0", port="80")
