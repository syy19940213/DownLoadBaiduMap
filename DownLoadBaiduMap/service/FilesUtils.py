#!/usr/bin/python

from traceback import format_exc

def write_file(fullname,data):
    try:
        fh = open(fullname,'w')
        fh.write(data)
        fh.close()
    except:
        print "write file error!"+format_exc()
    finally:
        fh.close()
