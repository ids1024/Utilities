#!/usr/bin/env python

import sys
import os
from subprocess import Popen

from importlib.machinery import SourceFileLoader

Popen(("xrdb","-merge",os.path.expanduser("~/.Xresources")))

conf = SourceFileLoader("conf", os.path.expanduser("~/.xinitrc.py")).load_module()
name, executable, depends = conf.environments[int(sys.argv[1])]

if depends:
    if hasattr(depends, '__iter__'):
        for i in depends:
            i.run()
    else:
        depends.run()
os.execlp(executable, executable)
