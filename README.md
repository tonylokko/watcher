# README #


### What is this repository for? ###

Watcher uploader for python 3
This script is a basic example of using the python watchdog module in conjunction with the requests module in order to monitor
files and upload them to a swarm cluster using scsp and token auth.
Currently the script runs in the foreground and will upload files on any newly created file in a monitored directory.


### How do I get set up? ###

Install python 3 if not already installed. 
Install the extra modules via pip3. 
Extra modules are 

-python-magic
-watchdog
-requests


The easiest way to do this is via pip. 
for linux you'll want to use 
pip3 install x
so 
pip3 install requests
pip3 install watchdog
pip3 install python-magic

For windows you'll still use pip3 but it'll be in the scripts directory where you installed python3.7
C:\Program Files\Python37\Scripts\pip 

when you navigate there via and admin command prompt you should be able to just go
pip install requests
pip install python-libmagic
pip install watchdog

you may also need 
pip install python-magic-bin

Make sure when installing python you install for all users which is a custom install of python for windows. 



modify the config.ini file to point to your destination whereever that is and add your auth token. 
Fomat for that is 
[domain]
domain : myexampledomain.com
#remember the leading and ending forward slash from bucketdestination
[bucket]
bucket : /mybucket/

[token]
token : tokenvalue

Changes in the qbranch are 
some filename parsing to attempt to garner details from the file name. 
gui.py, a test gui to create a config file and connection test to make the setup more user friendly. 


