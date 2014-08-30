#!/usr/bin/env python

import sys
import os
from subprocess import Popen

from ianxenv import Task

from importlib.machinery import SourceFileLoader
conf = SourceFileLoader("conf", os.path.expanduser("~/.xinitrc.py")).load_module()
name, executable, depends = conf.environments[int(sys.argv[1])]

Popen(("xrdb", "-merge", os.path.expanduser("~/.Xresources")))

if depends:
    if depends is Task:
        depends.run()
    else:
        for i in depends:
            i.run()

os.execlp(executable, executable)
