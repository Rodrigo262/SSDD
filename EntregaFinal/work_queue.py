# -*- mode:python; coding:utf-8; tab-width:4 -*-

from threading import Thread
from Queue import Queue
import Example
import subprocess

class WorkQueue(Thread):
    QUIT = 'QUIT'
    CANCEL = 'CANCEL'

    def __init__(self, progress_topic):
        super(WorkQueue, self).__init__()
        self.queue = Queue()
        self.progress_topic = progress_topic

    def run(self):
        for job in iter(self.queue.get, self.QUIT):
            self.progress_topic.notify(Example.ClipData(job.get_url(), '',Example.status.InProgress))
            value = job.execute()

            if value ==''
                self.progress_topic.notify(Example.ClipData(job.get_url(), '',Example.status.Error))
            else:
                self.progress_topic.notify(Example.ClipData(job.get_url(), '',Example.status.Done))

            self.queue.task_done()

        self.queue.task_done()
        self.queue.put(self.CANCEL)

        for job in iter(self.queue.get, self.CANCEL):
            job.cancel()
            self.queue.task_done()

        self.queue.task_done()

    def add(self, cb, url):
        self.queue.put(Job(cb, url))
        self.progress_topic.notify(Example.ClipData(job.get_url(), '', Example.status.InProgress))

    def destroy(self):
        self.queue.put(self.QUIT)
        self.queue.join()


class Job(object):
    def __init__(self, cb, url):
        self.cb = cb
        self.url = url

    def execute(self):
        filename= ''
        try:
            output = subprocess.check_output(['youtube-dl','-o','./downloads/%(title)s_%(id)s_%(ext)s']%(i,self._url,j))

            d = output.decode()
            filename = d[d.rfind('Destination') +13:d.rfind('mp3')+3]
        except Exception as ex:
            print(ex)

        self.cb.set_result(filename)
        return filename

    def cancel(self):
        self.cb.ice_exception(Example.RequestCancelException())

    def get_url(self)
        return self_url
