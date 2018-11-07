import cv2

class customizedTrackBar:
    def __init__(self, desiredStart, step, desiredEnd, defaultValue, description, windowName):
        self.description = description
        self.windowName = windowName

        self.defaultValue = defaultValue
        self.desiredStart = desiredStart
        self.step = int(1/step)
        self.desiredEnd = desiredEnd
        self.start = 0
        self.end = (self.desiredEnd - self.desiredStart)*self.step

        cv2.namedWindow(windowName, cv2.WINDOW_FREERATIO)
        self.createCutomizedTrackBar()
        self.setDefaultPosition()

    def createCutomizedTrackBar(self):
        cv2.createTrackbar(self.description, self.windowName, self.start, int(self.end), self.doNothing)

    def setDefaultPosition(self):
        ratio = (self.defaultValue - self.desiredStart)/(self.desiredEnd - self.desiredStart)
        defaultPosition = ratio * (self.end - self.start) + self.start
        cv2.setTrackbarPos(self.description, self.windowName, int(defaultPosition))

    def getValue(self):
        trackBarValue = cv2.getTrackbarPos(self.description, self.windowName)
        ratio = (trackBarValue - self.start)/(self.end - self.start)
        value = ratio *(self.desiredEnd - self.desiredStart) + self.desiredStart
        return value
    
    def doNothing(self,_):
        pass    
