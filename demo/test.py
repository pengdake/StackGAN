from gevent import monkey
monkey.patch_all()
import gevent
import requests
import base64
import uuid


def test():
    url = "http://127.0.0.1:80/model_app/stackgan/detect"
    files = {'file': open("/mxtg/code/StackGAN/Data/flowers/example_captions.txt", 'rb')}
    res = requests.post(url, files=files)
    data =  res.json()
    img = base64.b64decode(data["data"])
    with open("/stackgan_%s.jpg" % uuid.uuid1(), "wb") as f:
        f.write(img)


if __name__ == "__main__":
    spawn_list = []
    for i in range(3):
        spawn_list.append(gevent.spawn(test))
    gevent.joinall(spawn_list)