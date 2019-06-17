# This script is a basic example of using the python watchdog module in conjunction with the requests module in order to monitor
# files and upload them to a swarm cluster using scsp and token auth.
# Currently the script runs in the foreground and will upload files on any newly created file in a monitored directory.

# it requires 3 non standard modules , requests, watchdog and magic though magic isn't actually used yet.
# it is written for python3 and should work on any system that supports python3 though i've only tested it as of yet on linux.
import sys
import time
# this is used to read the file and we call the stat to get the filesize
import os
# will add logging later
import logging
# want to get the mimetype to add as header data for the upload
import magic
import watchdog
# watchdog is the module which scans the directories and the observer is the watching part of the watchdog
from watchdog.observers import Observer
# This is the filesystem event handler , there's a few different types this one just takes action on the filesystem
from watchdog.events import FileSystemEventHandler
# requests is used for the http upload.
import requests
import json
import psutil

#config from file test
import configparser
config = configparser.ConfigParser()
config.read("config.ini")
def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
        return dict1


domain = ConfigSectionMap("domain")['domain']
bucket = ConfigSectionMap("bucket")['bucket']
token = ConfigSectionMap("token")['token']


def get_platform():
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows',
    }
    if sys.platform not in platforms:
        return sys.platform
    return platforms[sys.platform]
operatingsystem = sys.platform
print(operatingsystem)


def pcapinterpret(itemname):
    if len(itemname) <= 31:
        xcommandsystemmeta = itemname[0]
        xhighwaymeta = itemname[1]
        xcshcontrollermeta = itemname[2]
        xdatafilteringmeta = itemname[3]
        xpcapsequencemeta = itemname[5:10]
        xdatatimefromfile = datetime.datetime.strptime(itemname[11:25], '%Y%m%d%H%M%S').isoformat()
        metas.clear()
        metas.update({'x-command-system-meta': xcommandsystemmeta})
        metas.update({'x-highway-system-meta': xhighwaymeta})
        metas.update({'x-cshcontroller-meta': xcshcontrollermeta})
        metas.update({'x-data-filtering-meta': xdatafilteringmeta})
        metas.update({'x-datetimefromfile-meta': xdatatimefromfile})
        return metas
    else:
        xcommandsystemmeta = itemname[0]
        xhighwaymeta = itemname[1]
        xcshcontrollermeta = itemname[2]
        xdatafilteringmeta = itemname[3]
        xtimeanddatemeta = itemname[5:24]
        xappidmeta = itemname[25:33]
        metas.clear()
        metas.update({'x-command-system-meta': xcommandsystemmeta})
        metas.update({'x-highway-system-meta': xhighwaymeta})
        metas.update({'x-cshcontroller-meta': xcshcontrollermeta})
        metas.update({'x-data-filtering-meta': xdatafilteringmeta})
        metas.update({'x-timeanddate-meta': xtimeanddatemeta})
        metas.update({'x-appid-meta': xappidmeta})
        return metas


# this class overrides the existing Filesystem event handler so we can have it do more stuff.
class Handler(FileSystemEventHandler):
    # on_created is a method that takes action only on newly created files.
    # there are also methods for modified and deleted etc
    def on_created(self, event):
        if event.is_directory:
            pass
        else:
        # here we're getting the name of the file / filepath for a new file.
            filenamefromwatchdog = event.src_path
            logging.info(filenamefromwatchdog)
            windowsfilename = filenamefromwatchdog.replace(os.sep, '/')
            print (windowsfilename)
        # here we're getting the filesize (sort of unnessacary
        # now but i'm thinking of adding conditional multipart based on size
            statinfo = os.stat(filenamefromwatchdog).st_size
            logging.info("the filesize in bytes is " + str(statinfo))
        # try magic, this is trying to get the mime-type of the file which is
            mimet = magic.from_file(filenamefromwatchdog, mime=True)
            print(mimet)
            logging.info("mimetype is" + mimet)
            print ('Filesize is:' + str(statinfo), 'bytes')

        # next section is the upload itself, vars for the destination have been set up in our config file
        # set the session up with the tokens etc
            s = requests.Session()
            cookies = {'token':  token }
            urlbucket=domain+bucket
        # here we pull the file name and open the file.
            filename = filenamefromwatchdog
            uploaddata = {'file': open(filenamefromwatchdog, 'rb')}
        # set up the headers
            mimet2 = "'{}'".format(mimet)
            content = {'Content-Type': mimet2 }
        # here we do the post.
            r = s.post(urlbucket + filename, data=open(filename, 'rb').read(), headers=content, cookies=cookies)
            logging.info("the result of the post was " + r.text)
            logging.info("the returncode for the http return headers were " + str(r.headers))
            logging.info("the http status code we got was " + str(r.status_code))
            print(r.text)

    def on_modified(self, event):
        if event.is_directory:
            pass
        else:
        # here we're getting the name of the file / filepath for a new file.
            filenamefromwatchdog = event.src_path
            logging.info(filenamefromwatchdog)
            windowsfilename = filenamefromwatchdog.replace(os.sep, '/')
            print (windowsfilename)
        # here we're getting the filesize (sort of unnessacary
        # now but i'm thinking of adding conditional multipart based on size
            statinfo = os.stat(filenamefromwatchdog).st_size
            logging.info("the filesize in bytes is " + str(statinfo))
        # try magic, this is trying to get the mime-type of the file which is
            mimet = magic.from_file(filenamefromwatchdog, mime=True)
            print(mimet)
            logging.info("mimetype is" + mimet)
            print ('Filesize is:' + str(statinfo), 'bytes')

        # next section is the upload itself, vars for the destination have been set up in our config file
        # set the session up with the tokens etc
            s = requests.Session()
            cookies = {'token':  token }
            urlbucket=domain+bucket
        # here we pull the file name and open the file.
            filename = filenamefromwatchdog
            uploaddata = {'file': open(filenamefromwatchdog, 'rb')}
        # set up the headers
            mimet2 = "'{}'".format(mimet)
            content = {'Content-Type': mimet2 }

        # here we do the post.
            r = s.post(urlbucket + filename, data=open(filename, 'rb').read(), headers=content, cookies=cookies)
            logging.info("the result of the post was " + r.text)
            logging.info("the returncode for the http return headers were " + str(r.headers))
            logging.info("the http status code we got was " + str(r.status_code))
            print(r.text)








if __name__ == "__main__":
    logging.basicConfig(filename='watcher3.log',level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    runningos = get_platform()
    print(runningos)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
