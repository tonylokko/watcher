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