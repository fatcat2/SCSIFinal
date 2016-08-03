import cv2


class Skeleton:
    linkageList = []
    lineColor = (203, 192, 255)

    def contains(self, a):
        return a in self.linkageList

    def addLink(self, start, end):
        self.linkageList.append((start, end))

    def getLink(self, x):
        return self.linkageList[x]

    def renderLink(self, image, index):
        cv2.line(image, self.linkageList[index][0].getCenterPoint(), self.linkageList[index][1].getCenterPoint(), self.lineColor,4)

    def renderAllLinks(self, image):
        for i in range(len(self.linkageList)):
            self.renderLink(image, i)

    def deleteLink(self, linkList):
        if linkList in self.linkageList:
            return self.linkageList.pop(self.linkageList.index(linkList))


class MidpointSkeleton(Skeleton):
    def renderLink(self, image, index):
        link = self.linkageList[index]
        points = (link[0].getCenterPoint(), link[1].getCenterPoint())
        cv2.line(image, points[0], points[1], self.lineColor, 4)
        point = ((points[0][0]+points[1][0])/2, (points[0][1]+points[1][1])/2,)
        cv2.circle(image, point, 3, (255, 0, 0), -1)