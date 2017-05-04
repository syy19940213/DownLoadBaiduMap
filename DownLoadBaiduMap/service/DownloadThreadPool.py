#!/usr/bin/python


import threading
import Queue
import os
from conf import config
from traceback import format_exc
import requests

## queue has no max
filequeue=Queue.Queue(maxsize=0)

sum = 0
count = 0

mutex = threading.Lock()

def run(func):
    try:
        global counter, count
        while not filequeue.empty():
            path = filequeue.get()
            try:
                fh = open(path,'r')
                for line in fh:
                    words = line.replace("\n","").split("\t")
                    z=words[0]
                    x=words[1]
                    y=words[2]
                    dir = config.DOWNLOAD_DIR+"/"+z+"/"+x
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    filename = config.DOWNLOAD_DIR+"/"+z+"/"+x+"/"+y+".jpg"
                    url = config.URL.format(x=x,y=y,z=z)
                    dowloadPic(url,filename)
                    if mutex.acquire():
                        count += 1
                        print "sum nums :%d    download nums:%d" % (sum,count)
                        mutex.release()
            except:
                print format_exc()
            finally:
                fh.close()
    except:
        print format_exc()



def dowloadPic(imageUrl,filePath):
    if os.path.exists(filePath) and config.IS_COVER == 1:
        os.remove(filePath)
        r = requests.get(imageUrl)
        with open(filePath, "wb") as code:
            code.write(r.content)
    elif not os.path.exists(filePath):
        r = requests.get(imageUrl)
        with open(filePath, "wb") as code:
            code.write(r.content)


threads = []

def init_pool():
    i=0;
    while i < config.POOL_SIZE:
        i += 1
        threads.append(threading.Thread(target=run,args=(i,)))


if __name__ == '__main__':
    init_pool()
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

    print "all over "