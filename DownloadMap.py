#!/usr/bin/python

import os
from conf import config
from service import FilesUtils
import time
from service import ThreadWork
from log import log


def write_xyz_file():
    data = ""
    file = 1
    nums = 0

    if not os.path.isdir(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)

    for parent, dirnames, filenames in os.walk(config.INPUT_DIR):
        for filename in filenames:
            if filename.endswith('.jpg'):
                path = parent + os.path.sep + filename
                path = path.replace(config.INPUT_DIR, "")
                path = path.replace(".jpg", "")
                path = path.split(os.path.sep)
                num = path.__len__()
                i = 1
                for word in path:
                    if i < num:
                        data += word + "\t"
                    else:
                        data += word + "\n"
                    i += 1
                nums +=1
                if nums % 10 == 0:
                    FilesUtils.write_file(config.OUTPUT_DIR+os.path.sep+str(file)+".dat", data)
                    file = file + 1
                    data=""
    ThreadWork.sum = nums
    FilesUtils.write_file(config.OUTPUT_DIR+os.path.sep+str(file)+".dat", data)
    return nums


if __name__ == '__main__':
    write_xyz_file()
    data = []
    sum = 0
    for parent, dirnames, filenames in os.walk(config.OUTPUT_DIR):
        for filename in filenames:
            sum = sum + 1
            data.append(os.path.join(parent,filename))
    ThreadWork.sum = sum
    start = time.time()
    work_manager = ThreadWork.WorkManager(data,config.POOL_SIZE)
    work_manager.wait_allcomplete()
    end = time.time()
    log.info( "cost all time: %s" % (end - start))

