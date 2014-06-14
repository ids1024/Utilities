#!/usr/bin/env python

#Statusbar script for dwm and dvtm

import os
import subprocess
import time
import alsaaudio
from email.utils import parseaddr
from email.parser import BytesHeaderParser
import abook
import psutil
import argparse

argparser = argparse.ArgumentParser(description='Dwm and Dvtm Status Bar')
argparser.add_argument('--dvtm', help='use with dvtm instead of dwm')
args = argparser.parse_args()

if args.dvtm:
    def setBar(text):
        with open(args.dvtm, 'w') as fifo:
            fifo.write(text)
    def formatText(text, **args):
        return text
else:
    def setBar(text):
        subprocess.call(["xsetroot", "-name", text])

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
        return formatted


def date():
    return time.strftime('%a %b %d %l:%M %P')

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
        return str(vol) + "% Volume"

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
    return formatText(str(percent) + "% CPU", fg=color)

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
    return formatText(str(percent) + "% RAM", fg=color)

def mail():
    inbox = "/home/ian/.mail/perebruin/INBOX"
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

