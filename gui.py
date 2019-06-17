#!/usr/bin/python3

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import requests

def writetofile():
    f = open("test.txt", "w+")
    res = txt.get()
    res2= txt2.get()
    res3= txt3.get()
    res4= txt4.get()
    res5= txt5.get()
    f.write("Log_file = " + res)
    f.write("\n")

    f.write("Watch_folder = " + res2)
    f.write("\n")
    f.write("Domain = " + res3)
    f.write("\n")
    f.write("Token = " + res4)
    f.write("\n")
    f.write("bucket = " + res5)
    f.close()

def browse_button():
    #allow user to select a directory and store it as a global var
    #called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)


def browse_buttonlog():
    #allow user to select a directory and store it as a global var
    #called log folder_path
    global logfolder_path
    filename = filedialog.askdirectory()
    logfolder_path.set(filename)
    print(filename)


def saveanddisplay():
    writetofile()
    saved.set("Saved")

def connectionpoll():
    #try a test connection with the entered details
    try:
        s = requests.Session()
        cookies = {'token': str(tokenvar.get())}
        urlbucket = str(domainvar.get()) + str(bucketvar.get())
        print(urlbucket)
        print(cookies)
        r = s.head(urlbucket, cookies=cookies)
        print(r.status_code)
        if r.status_code == requests.codes.ok:
            connectionstat.set(str(r.status_code) + " " + urlbucket + "token look ok you're good to go")
        else:
            connectionstat.set(urlbucket + " we tried to hit this and got " + str(r.status_code) + "http error check your input")
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Connect fail', 'Couldnt even try to connect there was anything entered in the fields')

top = Tk()
folder_path = StringVar()
logfolder_path = StringVar()
domainvar = StringVar()
tokenvar = StringVar()
bucketvar = StringVar()

top.geometry('950x400')
top.title("Directory Watcher")
lbl = Label(top, text="Log file location")
lbl.grid(column=0, row=0)

browsetologfile = Button(text = "Browse to logfile location", command=browse_button)
browsetologfile.grid(column=3, row=0)



txt = Entry(top,width=70,textvariable=folder_path)
txt.grid(column=1, row=0)

browsetowatcher = Button(text = "Browse to the directory you'd like to watch", command=browse_buttonlog)
browsetowatcher.grid(column=3, row=1)

lbl = Label(top, text="Directory to watch")
lbl.grid(column=0, row=1)



txt2 = Entry(top,width=70,textvariable=logfolder_path)
txt2.grid(column=1, row=1)



txt3 = Entry(top,width=70,textvariable=domainvar)
txt3.grid(column=1, row=2)

lbl = Label(top, text="Storage domain you want to write to")
lbl.grid(column=0, row=2)



txt4= Entry(top,width=70,textvariable=tokenvar)
txt4.grid(column=1, row=3)


lbl = Label(top, text="Token credentials you will use")
lbl.grid(column=0, row=3)



txt5 = Entry(top,width=70,textvariable=bucketvar)
txt5.grid(column=1, row=4)

lbl = Label(top, text="Bucket that you will write to")
lbl.grid(column=0, row=4)



btn = Button(top, text="Save All", command=saveanddisplay)
btn.grid(column=1, row=6)
saved = StringVar()
lbl2 = Label(top, textvariable=saved)
lbl2.grid(column=1, row=7)



btn = Button(top, text="Connection Test", command=connectionpoll)
btn.grid(column=1, row=8)
connectionstat = StringVar()
lbl3 = Label(top, textvariable=connectionstat)
lbl3.grid(column=1, row=9)







top.mainloop()

