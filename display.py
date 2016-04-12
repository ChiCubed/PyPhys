# view.py - Handles a camera and all the icky pygame stuff.
# Copyright (C) 2016  Albert Smith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
from constants import FPS
from geometry import *
import sys

import thread

class Camera(object):
	def __init__(self, pos=Vector2D(0,0), zoom = 100, resizable = True, screen=None):
		"""
		screen designates pygame surface to draw to
		pos is the central position of the camera
		zoom is the number of pixels per metre
		"""
		pygame.init()

		if screen is None:
			screen = pygame.display.get_surface()
			if screen is None:
				if resizable:
					screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
				else:
					screen = pygame.display.set_mode((800, 600))
		self.w, self.h = screen.get_size()
		self.screen = screen
		self.clock = pygame.time.Clock()
		self.pos = pos
		self.zoom = zoom

		self.cinematic = False

		# What a great idea
		self.handles = {pygame.QUIT: ("I", self.quit),
						pygame.VIDEORESIZE: ("I", self.handleResize)
						}
		self.keyvals = {}
		self.mousevals = {}

		self.toRunEveryFrame = []

	def addHandle(self, key, value):
		self.handles[key] = value

	def addKeyValue(self, key, value):
		self.keyvals[key] = value

	def addMouseValue(self, key, value):
		self.mousevals[key] = value

	def addHandles(self, handles):
		"""
		Adds new handles.
		Overwrites old ones.
		"""
		self.handles.update(handles)

	def addKeyValues(self, keyvals):
		"""
		Same as above except for key values.
		"""
		self.keyvals.update(keyvals)

	def addMouseValues(self, mousevals):
		"""
		Same as above except for mouse values.
		"""
		self.mousevals.update(mousevals)

	def getMousePos(self):
		return pygame.mouse.get_pos()

	def posToPygame(self, pos):
		return (int((pos[0] - self.pos.x) * self.zoom + self.w / 2), \
				int((self.h / 2) - (pos[1] - self.pos.y) * self.zoom))

	def posFromPygame(self, pos):
		return Vector2D((pos[0] - self.w/2.0)/self.zoom + self.pos.x, \
						(self.h/2.0 - pos[1])/self.zoom + self.pos.y)

	def lengthToPygame(self, length):
		return int(length * self.zoom)

	def lengthFromPygame(self, length):
		return length / (self.zoom * 1.0)

	def runInBackground(self, func, args):
		thread.start_new_thread(func, tuple(args))

	def enableCinematic(self):
		self.cinematic = True

	def disableCinematic(self):
		self.cinematic = False

	def runEveryFrame(self, func, args, numframes, final = None, finalArgs = ()):
		self.toRunEveryFrame.append([func, args, 0, numframes, final, finalArgs])

	def evalTimedFunc(self, index):
		info = self.toRunEveryFrame[index]
		if (info[2] == info[3] - 1) and info[4] is not None:
			info[4](*info[5])

		newargs = []
		for e in info[1]:
			if e == "frame":
				newargs.append(info[2])
			elif e == "numframes":
				newargs.append(info[3])
			else:
				newargs.append(e)
		info[0](*newargs)

		info[2] += 1

	def manageHandles(self):
		for event in pygame.event.get():
			if event.type in self.handles:
				# I is internal, i.e. does not require this object
				# E is external, i.e. modifies this object
				if self.handles[event.type][0] == "I":
					self.handles[event.type][1](event)
				if self.handles[event.type][0] == "E":
					self.handles[event.type][1](event, self)

		if "KEY" in self.handles:
			keys = pygame.key.get_pressed()
			for i in xrange(len(keys)):
				if keys[i] and i in self.keyvals:
					if self.handles["KEY"][0] == "I":
						self.handles["KEY"][1](self.keyvals[i])
					if self.handles["KEY"][0] == "E":
						self.handles["KEY"][1](self.keyvals[i], self)

		if "MOUSE" in self.handles:
			down = pygame.mouse.get_pressed()
			for i in xrange(len(down)):
				if down[i] and i in self.mousevals:
					if self.handles["MOUSE"][0] == "I":
						self.handles["MOUSE"][1](self.mousevals[i])
					if self.handles["MOUSE"][0] == "E":
						self.handles["MOUSE"][1](self.mousevals[i], self)


	def getKeyName(self, key):
		return pygame.key.name(key)

	def handleResize(self, event):
		self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
		self.w, self.h = event.size

	def update(self, bodies):
		self.manageHandles()

		self.screen.fill(pygame.color.THECOLORS['white'])
		for body in bodies:
			self.draw(body)

		for i in xrange(len(self.toRunEveryFrame)):
			self.evalTimedFunc(i)
		# Clean up the expired ones
		self.toRunEveryFrame = [i for i in self.toRunEveryFrame if i[2] < i[3]]

		pygame.display.flip()
		self.clock.tick(FPS)

	def contains(self, body):
		if isinstance(body, Circle):
			return ((body.center.x + body.r > self.pos.x - (self.w*0.5 / self.zoom)) and
					(body.center.x - body.r < self.pos.x + (self.w*0.5 / self.zoom)) and
					(body.center.y + body.r > self.pos.y - (self.h*0.5 / self.zoom)) and
					(body.center.y - body.r < self.pos.y + (self.h*0.5 / self.zoom)))
		if isinstance(body, Rectangle):
			return ((body.minBounds.center.x + body.minBounds.w > self.pos.x - (self.w*0.5 / self.zoom)) and
					(body.minBounds.center.x - body.minBounds.w < self.pos.x + (self.w*0.5 / self.zoom)) and
					(body.minBounds.center.y + body.minBounds.h > self.pos.y - (self.h*0.5 / self.zoom)) and
					(body.minBounds.center.y - body.minBounds.h < self.pos.y + (self.h*0.5 / self.zoom)))

	def draw(self, body):
		if not self.contains(body):
			print "OUTSIDE"
			return
		if isinstance(body, Circle):
			pygame.draw.circle(self.screen, pygame.color.THECOLORS['black'], \
				self.posToPygame(body.center), self.lengthToPygame(body.r))
		if isinstance(body, Rectangle):
			pygame.draw.polygon(self.screen, pygame.color.THECOLORS['black'], \
				map(self.posToPygame, body))

	def translate(self, vector):
		if not self.cinematic:
			self.pos += vector

	def translateRelative(self, vector):
		if not self.cinematic:
			self.pos += Vector2D.from_list(vector) / self.zoom

	def scaleLinear(self, amount):
		if not self.cinematic:
			self.zoom += amount

	def scale(self, amount):
		if not self.cinematic:
			self.zoom *= amount

	def quit(self, event = None):
		pygame.quit()
		if event is None:
			sys.exit(0)
		sys.exit(pygame.event.event_name(event.type))