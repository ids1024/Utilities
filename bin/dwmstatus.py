#!/usr/bin/env python

#Statusbar script for dwm and dvtm
#TODO: Warnings and errors, string formatting


import os
import subprocess
import time
import alsaaudio
from email.utils import parseaddr
from email.parser import BytesHeaderParser
import abook
import psutil
import argparse
import shutil
import logging

tmpdir = "/tmp/dwmstatus"

logging.basicConfig(
        filename="/tmp/dwmstatus.log",
        level=logging.INFO,
        datefmt='%s', #Unix time
        format="%(asctime)s %(levelname)s:%(message)s")

argparser = argparse.ArgumentParser(description='Dwm and Dvtm Status Bar')
argparser.add_argument('--dvtm', help='Use with dvtm instead of dwm')
argparser.add_argument('--stop', action='store_true', help='Stop server')
args = argparser.parse_args()

if os.path.exists(tmpdir):
    try:
        with open(tmpdir + "/pidfile") as file:
            os.kill(int(file.read()), 0) #test if process exists
        if args.stop:
            cmd = "exit"
        elif args.dvtm:
            cmd = "dvtm " + args.dvtm
        else:
            cmd = "dwm " + os.environ["DISPLAY"]
        with open(tmpdir + "/ctl", 'w') as fifo:
            fifo.write(cmd)
        exit()

    except OSError: # is os.kill fails
        shutil.rmtree(tmpdir)

if args.stop:
    exit()

if os.fork() != 0: #Run in background
    exit()

os.mkdir(tmpdir)
with open(tmpdir + "/pidfile", 'w') as file:
    file.write(str(os.getpid()))

os.mkfifo(tmpdir + "/ctl")
def opener(file, flags):
    return os.open(file, flags | os.O_NONBLOCK)
ctlfifo = open(tmpdir + "/ctl", opener=opener)
dvtmfifos = set()
dwmsessions = set()


if args.dvtm:
    dvtmfifos.add(args.dvtm)
else:
    dwmsessions.add(os.environ["DISPLAY"])

def setDvtmBar(text, fifopath):
    try:
        with open(fifopath, 'w', opener=opener) as fifo:
            fifo.write(text + '\n')
    except OSError: #Not open for reading
        logging.info("Discarding " + fifopath)
        removefifos.append(fifopath)

def setDwmBar(text, display):
    if subprocess.call(["xsetroot", "-name", text],env={"DISPLAY":display}) != 0:
        removedisplays.append(display)

def formatText(text, bg=None, fg=None, bold=False):
    formatted = ""
    formatted += "<span"
    if bg:
        formatted += ' background="' + bg + '"'
    if fg:
        formatted += ' foreground="' + fg + '"'
    if bold:
        formatted += ' weight="bold"'
    formatted += ">" + text + "</span>"
    return (text, formatted)

def exitprogram():
    shutil.rmtree(tmpdir)
    ctlfifo.close()
    exit()




def date():
    return formatText(time.strftime('%a %b %d %I:%M %p'))

def ssid():
    output = subprocess.check_output(('iwconfig','wlan0')).decode().split('\n')[0]
    if 'off/any' in output:
        return None
    else:
        return formatText(output.split('"')[1])

def volume():
    mixer = alsaaudio.Mixer("Master")
    vol = mixer.getvolume()[0]
    if mixer.getmute()[0]:
        return formatText(str(vol) + "% Muted",fg="grey")
    else:
        return formatText("{0}% Volume".format(vol))

def cpu():
    percent = (round(psutil.cpu_percent()))
    if percent < 20:
        color = None
    elif percent < 50:
        color = "yellow"
    elif percent < 80:
        color = "orange"
    else:
        color = "red"
    return formatText("{0}% CPU".format(percent),fg=color)

def ram():
    percent = round(psutil.virtual_memory().percent)
    if percent < 20:
        color = None
    elif percent < 50:
        color = "yellow"
    elif percent < 80:
        color = "orange"
    else:
        color = "red"
    return formatText("{0}% RAM".format(percent),fg=color)

def mail():
    inbox = "/home/ian/.mail/perebruin/INBOX"
    addressbook = abook.get_abook()
    parser = BytesHeaderParser()
    os.chdir(inbox+"/new")
    unread = False
    for i in os.listdir():
        with open(i, 'rb') as file:
            email = parser.parse(file)
        if parseaddr(email.get('from'))[1] in addressbook:
            return formatText('  ✉',fg="red")
        unread = True
    if unread:
        return formatText('  ✉')
    return formatText('')

items = (volume, cpu, ram, ssid, date)
divider = ' ❧ '


while True:
    for line in ctlfifo.read().splitlines():
        words = line.split()
        if words[0] == "dwm":
            dwmsessions.add(words[1])
        elif words[0] == "dvtm":
            dvtmfifos.add(words[1])
        elif words[0] == "exit":
            logging.info("Exiting.")
            exitprogram()

    if len(dwmsessions) == 0 and len(dvtmfifos) == 0:
        logging.info("No more clients. Exiting.")
        exitprogram()

    output = []
    formatedoutput = []
    for i in items:
       value = i()
       if value:
           output.append(value[0])
           formatedoutput.append(value[1])
    outstring = divider.join(output) + mail()[0]
    formatedoutstring = divider.join(formatedoutput) + mail()[1]

    removedisplays = [] #Cannot remove while iterating over set TODO: Better way.
    for display in dwmsessions:
        setDwmBar(formatedoutstring, display)
    for i in removedisplays: dwmsessions.discard(i)

    removefifos = []
    for fifo in dvtmfifos:
        setDvtmBar(outstring, fifo)
    for i in removefifos: dvtmfifos.discard(i)

    time.sleep(1)
