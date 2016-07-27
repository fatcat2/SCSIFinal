import cv2


class Skeleton:
    linkageList = []
    lineColor = (203, 192, 255)

    def __init__(self, initLinks=[]):
        self.linkageList = initLinks
        pass

    def addLink(self, to):
        self.linkageList.append(to)

    def getLink(self, x):
        return self.linkageList[x]

    def renderLink(self, image, index):
        cv2.line(image, self.linkageList[index][0], self.linkageList[index][1], self.lineColor)

    def renderAllLinks(self, image):
        for x in self.linkageList:
            cv2.line(image, x[0], x[1], self.lineColor)