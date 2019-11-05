from gevent import monkey
monkey.patch_all()
import gevent
import requests
import base64
import uuid


def test():
    url = "http://127.0.0.1:80/detect"
    files = {'file': open("/mxtg/code/StackGAN/Data/flowers/example_captions.txt", 'rb')}
    res = requests.post(url, files=files)
    if res.status_code == 400:
        print res.text
        return
    else:
        print "Success"


if __name__ == "__main__":
    spawn_list = []
    for i in range(3):
        spawn_list.append(gevent.spawn(test))
    gevent.joinall(spawn_list)
