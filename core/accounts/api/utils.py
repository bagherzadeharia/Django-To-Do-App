import threading

class EmailThread(threading.Thread):
    def __init__(self, emailObject):
        threading.Thread.__init__(self)
        self.emailObject = emailObject

    def run(self):
        self.emailObject.send()