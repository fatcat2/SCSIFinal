import cv2
class Skeleton:
	linkageList = []
	def __init__(self):
		pass
	def addLink(self, to):
		linkageList.append(to)
	def getLink(self, x):
		return linkageList[x]
	def renderLink(self, image, index):
		cv2.line(image, linkageList[index][0], linkageList[index][1], (203, 192, 255))
		