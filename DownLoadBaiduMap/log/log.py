#!/usr/bin/python
import logging
import logging.config



logging.config.fileConfig("log/logger.conf")


def info(message):
    logger = logging.getLogger("info")
    logger.info(message)

def warn(message):
    logger = logging.getLogger("info")
    logger.warn(message)

def error(message):
    logger = logging.getLogger("error")
    logger.error(message)



def testfun():
    info("test")



if __name__ == '__main__':
    info("this is test")
    warn("this is warn")
    try:
        testfun(1)
    except TypeError, e:
        error("the type is error")

