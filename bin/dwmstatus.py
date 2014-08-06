#!/usr/bin/env python

#Statusbar script for dwm and dvtm
#TODO: Warnings and errors, string formatting, proper mail() integration


import os
import subprocess
import time
import argparse
import shutil
import logging

#Use with open() to open a fifo in nonblocking mode
def opener(file, flags):
    return os.open(file, flags | os.O_NONBLOCK)


from importlib.machinery import SourceFileLoader
conf = SourceFileLoader("conf", os.path.expanduser("~/.dwmstatusrc")).load_module()

logging.basicConfig(
        filename="/tmp/dwmstatus.log",
        level=logging.INFO,
        datefmt='%s', #Unix time
        format="%(asctime)s %(levelname)s:%(message)s")

argparser = argparse.ArgumentParser(description='Dwm and Dvtm Status Bar')
argparser.add_argument('--dvtm', help='Use with dvtm instead of dwm')
argparser.add_argument('--stop', action='store_true', help='Stop server')
args = argparser.parse_args()

if os.path.exists(conf.tmpdir):
    try:
        with open(conf.tmpdir + "/pidfile") as file:
            os.kill(int(file.read()), 0) #test if process exists
        if args.stop:
            cmd = "exit"
        elif args.dvtm:
            cmd = "dvtm " + args.dvtm
        else:
            cmd = "dwm " + os.environ["DISPLAY"]
        with open(conf.tmpdir + "/ctl", 'w') as fifo:
            fifo.write(cmd)
        exit()

    except OSError: # is os.kill fails
        shutil.rmtree(conf.tmpdir)

if os.fork() != 0: #Run in background
    exit()

os.mkdir(conf.tmpdir)
with open(conf.tmpdir + "/pidfile", 'w') as file:
    file.write(str(os.getpid()))

os.mkfifo(conf.tmpdir + "/ctl")
ctlfifo = open(conf.tmpdir + "/ctl", opener=opener)
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
        dvtmfifos.discard(fifopath)

def setDwmBar(text, display):
    if subprocess.call(("xsetroot", "-name", text),env={"DISPLAY":display}) != 0:
        dwmsessions.discard(display)

def exitprogram():
    shutil.rmtree(conf.tmpdir)
    ctlfifo.close()
    exit()



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

    output = zip(*filter(None, (i() for i in conf.items)))
    mail = conf.mail()
    outstring = conf.divider.join(next(output)) + mail[0]
    formatedoutstring = conf.divider.join(next(output)) + mail[1]

    for display in dwmsessions.copy():
        setDwmBar(formatedoutstring, display)

    for fifo in dvtmfifos.copy():
        setDvtmBar(outstring, fifo)

    if len(dwmsessions) == 0 and len(dvtmfifos) == 0:
        logging.info("No more clients. Exiting.")
        exitprogram()

    time.sleep(1)
