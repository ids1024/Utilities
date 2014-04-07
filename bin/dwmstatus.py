#!/usr/bin/env python

#Statusbar script for dwm and dvtm

import os
import subprocess
import time
import alsaaudio
import threading
from email.utils import parseaddr
from email.parser import BytesHeaderParser
import abook
import psutil
import argparse

argparser = argparse.ArgumentParser(description='Dwm and Dvtm Status Bar')
argparser.add_argument('--dvtm', help='use with dvtm instead of dwm')
args = argparser.parse_args()

def setBarDwm(text):
    subprocess.call(["xsetroot", "-name", text])

def setBarDvtm(text):
    with open(args.dvtm, 'w') as fifo:
        fifo.write(text)


def pangoFormat(text, bg=None, fg=None, bold=False):
    formatted = ""
    formatted += "<span"
    if bg:
        formatted += ' background="' + bg + '"'
    if fg:
        formatted += ' foreground="' + fg + '"'
    if bold:
        formatted += ' weight="bold"'
    formatted += ">" + text + "</span>"
    return formatted

def nullFormat(text, **args):
    return text

if args.dvtm:
    setBar = setBarDvtm
    formatText = nullFormat
else:
    setBar = setBarDwm
    formatText = pangoFormat


def date():
    return time.strftime('%a %b %d %I:%M %p')

def ssid():
    output = subprocess.check_output(('iwconfig','wlan0')).decode().split('\n')[0]
    if 'off/any' in output:
        return None
    else:
        return output.split('"')[1]

def volume():
    mixer = alsaaudio.Mixer("Master")
    vol = mixer.getvolume()[0]
    if mixer.getmute()[0]:
        return formatText(str(vol) + "% Muted",fg="grey")
    else:
        return "{0}% Volume".format(vol)

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
    inbox = "/home/ian/.mail/INBOX"
    addressbook = abook.get_abook()
    unread = False
    parser = BytesHeaderParser()
    os.chdir(inbox+"/new")
    for i in os.listdir():
        with open(i, 'rb') as file:
            email = parser.parse(file)
        if parseaddr(email.get('from'))[1] in addressbook:
            unread = True
            break
    if unread:
        return formatText('✉',fg="red")
    return None


items = (volume, cpu, ram, ssid, date, mail)
divider = ' ❧ '

while True:
    output = []
    for i in items:
       value = i()
       if value:
           output.append(value)
    setBar(divider.join(output))
    time.sleep(1)

