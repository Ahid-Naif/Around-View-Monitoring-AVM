import cv2
from threading import Thread
import time

class CalibrationTimer(object):
    def __init__(self, maxValue):
        self.timerValue = maxValue
        self.stopped = False
    def start(self):
        Thread(target=self.count, args=()).start()
        self.resetTimer()
    
    def count(self):
        while True:
            time.sleep(1)
            self.timerValue = 3
            if self.timerValue < 0:
                self.resetTimer()
            
            if self.stopped:
                return 

    def readTimer(self):
        return self.timerValue

    def resetTimer(self):
        self.timer = 5
        self.stopped = False
    
    def stop(self):
        self.stopped = True
    