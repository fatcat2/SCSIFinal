import cv2
class Skeleton:
	linkageList = []
	lineColor = (203, 192, 255)
	def __init__(self, initLinks=[]):
		linkageList=initLinks
		pass
	def addLink(self, to):
		linkageList.append(to)
	def getLink(self, x):
		return linkageList[x]
	def renderLink(self, image, index):
		cv2.line(image, linkageList[index][0], linkageList[index][1], lineColor)
	def renderAllLinks(self, image):
		for x in linkageList:
			cv2.line(image, x[0], x[1], lineColor) 