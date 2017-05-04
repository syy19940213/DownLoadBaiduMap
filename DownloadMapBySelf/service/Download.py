import os,urllib2
from service import config
from traceback import format_exc

def do_job(x,y,z):


    try:
         filename = config.DOWNLOAD_DIR + os.path.sep + z + os.path.sep + x + os.path.sep + y + ".jpg"
         if not os.path.exists(filename):
             dir = config.DOWNLOAD_DIR + os.path.sep + z + os.path.sep + x
             if not os.path.exists(dir):
                 os.makedirs(dir)
             url = config.URL.format(x=x, y=y, z=z)
             dowloadPic(url, filename)
             print "download file:"  + z + os.path.sep + x + os.path.sep + y + ".jpg"

    except:
        print (format_exc())





def dowloadPic(imageUrl,filePath):
    f = urllib2.urlopen(imageUrl)
    data = f.read()
    with open(filePath, "wb") as code:
        code.write(data)