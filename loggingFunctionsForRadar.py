import logging
import io
import collections


#FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s - %(pathname)s - %(lineno)d — %(message)s")
#FORMATTER = logging.Formatter(" %(levelname)s - %(asctime)s — %(funcName)s - %(message)s")
FORMATTER = logging.Formatter("%(levelname)s:%(message)s")



class FIFOIO(io.TextIOBase):
    def __init__(self, size, *args):
        self.maxsize = size
        io.TextIOBase.__init__(self, *args)
        #deque: collections, list like container with fast appends and pop on either end
        #create a new deque object, deque="double ended object."
        self.deque = collections.deque()
    def getvalue(self):
        return ''.join(self.deque)
    def write(self, x):
        self.deque.append(x)
        self.shrink()
    def shrink(self):
        if self.maxsize is None:
            return
        size = sum(len(x) for x in self.deque)
        while size > self.maxsize:
            x = self.deque.popleft()
            size -= len(x)


class loggerFunctions():
    def buildLogger():
        global logger
        logger = logging.getLogger('basic_logger')
        logger.setLevel(logging.DEBUG)
        global log_capture_string
        log_capture_string = FIFOIO(256)
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.DEBUG)

        ch.setFormatter(FORMATTER)

        logger.addHandler(ch)

    def sendToLogger(text):
        logger.debug(text)
        log_contents = log_capture_string.getvalue()        
        print(log_contents)
        return log_contents

    def closeLoggerFile():
        log_capture_string.close()
        



   
   

