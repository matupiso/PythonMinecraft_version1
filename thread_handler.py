from settings import *
from terrian_gen import get_height
import threading
from types import FunctionType

class ThreadHandler:
    def __init__(self, app):
        self.app = app
        self.thread_count = 0
        self.threads = {}
        self.threads_to_add = []

    def update(self):
        if self.thread_count < 4 and len(self.threads_to_add) > 0:
            self.add_thread(*self.threads_to_add[0])
            del self.threads_to_add[0]

    def add_thread(self, name, threadfunc, endfunc):

        if self.thread_count < 4:
            self.threads[name] = [endfunc, threading.Thread(target=threadfunc)]
            self.threads[name][1].start()
            self.thread_count += 1
        else:
            self.threads_to_add.append([name, threadfunc, endfunc])
        