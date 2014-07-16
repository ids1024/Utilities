#!/usr/bin/env python

import sys
import os
from subprocess import Popen

from importlib.machinery import SourceFileLoader

Popen(("xrdb","-merge",os.path.expanduser("~/.Xresources")))

conf = SourceFileLoader("conf", os.path.expanduser("~/.xinitrc.py")).load_module()
environment = conf.environments[int(sys.argv[1])]

if environment[2]:
    if hasattr(environment[2], '__iter__'):
        for i in environment[2]:
            i.run()
    else:
        environment[2].run()
os.execlp(environment[1], environment[1])

