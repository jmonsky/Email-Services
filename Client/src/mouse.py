from time import time


def dist(p1, p2):
	return ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**(1/2)

class Mouse(object):
	def __init__(self):
		self.x = 0
		self.y = 0
		self.dx = 0
		self.dy = 0
		self.buttons = [0,0,0,0,0,0,0,0]
		self.drags = []
		for i in self.buttons:
			self.drags.append([(0,0), (0,0)])
		self.mouseClicked = None
		self.mouseDragged = None
	def setFunctions(self, mouseClicked, mouseDragged, mouseMoved, mousePressed, mouseReleased):
		self.mouseClicked = mouseClicked
		self.mouseDragged = mouseDragged
		self.mouseMoved = mouseMoved
		self.mousePressed = mousePressed
		self.mouseReleased = mouseReleased
	def mouseDown(self, x, y, button):
		if self.buttons[button] == 0:
			self.x = x
			self.y = y
			self.buttons[button] = 1
			self.drags[button][0] = (x, y)
			self.press(x, y, button)
	def mouseUp(self, x, y, button):
		if self.buttons[button] == 1:
			self.x = x
			self.y = y
			self.buttons[button] = 0
			self.drags[button][1] = (x, y)
			self.release(x, y, button)
			if dist(self.drags[button][0], self.drags[button][1]) < 25:
				self.click(x, y, button)
			else:
				self.drag(self.drags[button], button)
			
	def move(self, x, y):
		self.dx = x-self.x
		self.dy = y-self.y
		self.x = x
		self.y = y
		self.mouseMove(x, y, self.dx, self.dy)
	def click(self, x, y, button):
		if self.mouseClicked != None:
			self.mouseClicked(x,y,button)
		else:
			pass
	def drag(self, drag, button):
		if self.mouseDragged != None:
			self.mouseDragged(drag, button)
		else:
			pass
	def mouseMove(self, x, y, dx, dy):
		if self.mouseMoved != None:
			self.mouseMoved(x, y, dx, dy, self.buttons)
		else:
			pass
	def press(self, x, y, button):
		if self.mousePressed != None:
			self.mousePressed(x, y, button)
		else:
			pass
	def release(self, x, y, button):
		if self.mouseReleased != None:
			self.mouseReleased(x, y, button)
		else:
			pass
