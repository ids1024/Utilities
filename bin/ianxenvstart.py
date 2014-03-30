#!/usr/bin/env python

import sys
from subprocess import Popen,call

from importlib.machinery import SourceFileLoader

Popen(("xrdb","-merge","/home/ian/.Xresources"))

conf = SourceFileLoader("conf","/home/ian/.xinitrc.py").load_module()
environment = conf.environments[int(sys.argv[1])]

if environment[2]:
    if getattr(environment[2], '__iter__', False):
        for i in environment[2]:
            i.run()
    else:
        environment[2].run()
call(environment[1])

