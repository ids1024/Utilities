from subprocess import Popen,call

class Task:
    command = None
    process = None
    background = None
    def __init__(self, *command, background=False):
        self.command = command
        self.background = background

    def run(self):
        self.process = Popen(self.command)
        if not self.background:
            self.process.wait()


class Environments:
    def __init__(self):
        self.list=[]

    def add(self,*args,name=None,Title=None):
        self.list.append(*args,name=name,title=title)
