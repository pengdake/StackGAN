from gevent import monkey
monkey.patch_all()
import gevent
import requests
import random


def test():
    url = "http://127.0.0.1:80/model_app/stackgan/detect"
    files = {'file': open("/mxtg/code/StackGAN/Data/flowers/examples_captions.txt", 'rb')}
    res = requests.post(url, files=files)
    data =  res.json()
    print "%d:%s" %(random.randint(10), data)


if __name__ == "__main__":
    spawn_list = []
    for i in range(3):
        spawn_list.append(gevent.spawn(test))
    gevent.joinall(spawn_list)