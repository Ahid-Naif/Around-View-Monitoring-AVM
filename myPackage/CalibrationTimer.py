import cv2

class CalibrationTimer(object):
    def __init__(self, maxValue):
        self.initialTimerValue = maxValue
        self.timerValue = maxValue
        self.stopped = False
    
    def count(self): 
        while True:           
            self.timerValue -= 1
            if self.timerValue < 0:
                self.resetTimer()
            if self.stopped:
                return
    
    def start(self):
        self.resetTimer()

    def readTimer(self):
        return self.timerValue

    def resetTimer(self):
        self.timerValue = self.initialTimerValue
        self.stopped = False
    
    def stop(self):
        self.stopped = True
    