import cv2


class Skeleton:
    linkageList = []
    lineColor = (203, 192, 255)

    def __init__(self, initLinks=[]):
        self.linkageList = initLinks
        pass

    def addLink(self, start, end):
        self.linkageList.append((start, end))

    def getLink(self, x):
        return self.linkageList[x]

    def renderLink(self, image, index):
        cv2.line(image, self.linkageList[index][0], self.linkageList[index][1], self.lineColor,4)

    def renderAllLinks(self, image):
        for x in self.linkageList:
            cv2.line(image, tuple(x[0].getCenterPoint()), tuple(x[1].getCenterPoint()), self.lineColor,4)

    def deleteLink(self, linkList):
        if linkList in self.linkageList:
            return self.linkageList.pop(self.linkageList.index(linkList))