# !/usr/bin/env python


import Queue
import threading
import time
import os
import urllib2
from conf import config
from traceback import format_exc
from log import log

class WorkManager(object):
    def __init__(self, filelist,pool_size ):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(filelist)
        self.__init_thread_pool(pool_size)



    def __init_thread_pool(self, thread_num):
        for i in range(thread_num):
            self.threads.append(Work(self.work_queue))



    def __init_work_queue(self, filelist):
        for filepath in filelist:
            self.add_job(do_job, filepath)



    def add_job(self, func, filepath):
        self.work_queue.put((func, filepath))



    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive(): item.join()


class Work(threading.Thread):
    def __init__(self, work_queue):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.start()

    def run(self):

        while True:
            try:
                do, filepath = self.work_queue.get(block=False)
                do(filepath)
                self.work_queue.task_done()
            except:
                break


mutex = threading.Lock()
count = 0
sum = 0


def do_job(path):
    global mutex, count

    try:
        fh = open(path, 'r')
        for line in fh:
            words = line.replace("\n", "").split("\t")
            z = words[0]
            x = words[1]
            y = words[2]
            dir = config.DOWNLOAD_DIR + os.path.sep + z + os.path.sep + x
            if not os.path.exists(dir):
                os.makedirs(dir)
            filename = config.DOWNLOAD_DIR + os.path.sep + z + os.path.sep + x + os.path.sep + y + ".jpg"
            url = config.URL.format(x=x, y=y, z=z)
            dowloadPic(url, filename)
        mutex.acquire()
        count = count + 1
        log.info("sum nums :%d    download nums:%d" % (sum, count))
        mutex.release()
    except:
        log.error(format_exc())
    finally:
        fh.close()




def dowloadPic(imageUrl,filePath):
    if os.path.exists(filePath) and config.IS_COVER == 1:
        os.remove(filePath)
        f = urllib2.urlopen(imageUrl)
        data = f.read()
        with open(filePath, "wb") as code:
            code.write(data)
    elif not os.path.exists(filePath):
        f = urllib2.urlopen(imageUrl)
        data = f.read()
        with open(filePath, "wb") as code:
            code.write(data)

if __name__ == '__main__':
    start = time.time()
    work_manager = WorkManager(100, 10)
    work_manager.wait_allcomplete()
    end = time.time()
    print "cost all time: %s" % (end - start)