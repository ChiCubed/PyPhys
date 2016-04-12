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
from util import Vector2D
from constants import FPS
from geometry import *
import sys

class Camera(object):
	def __init__(self, pos=Vector2D(0,0), zoom = 100, screen=None):
		"""
		screen designates pygame surface to draw to
		pos is the central position of the camera
		zoom is the number of pixels per metre
		"""
		pygame.init()

		if screen is None:
			screen = pygame.display.get_surface()
			if screen is None:
				screen = pygame.display.set_mode((800, 600))
		self.screen = screen
		self.clock = pygame.time.Clock()
		self.pos = pos
		self.zoom = zoom

		# What a great idea
		self.handles = {pygame.QUIT: self.quit,
						"KEY": self.translate,
						}
		self.keyvals = {pygame.K_LEFT: (-.1,  0),
						pygame.K_RIGHT:( .1,  0),
						pygame.K_UP:   (  0, .1),
						pygame.K_DOWN: (  0,-.1),
						}

	def posToPygame(self, pos):
		return (int((pos.x - self.pos.x) * self.zoom + self.screen.get_width() / 2), \
				int((self.screen.get_height() / 2) - (pos.y - self.pos.y) * self.zoom))

	def lengthToPygame(self, length):
		return length * zoom

	def manageHandles(self):
		for event in pygame.event.get():
			if event.type in self.handles:
				self.handles[event.type](event)

		if "KEY" in self.handles:
			keys = pygame.key.get_pressed()
			for i in xrange(len(keys)):
				if keys[i] and i in self.keyvals:
					self.handles["KEY"](self.keyvals[i])

	def update(self, bodies):
		self.manageHandles()

		self.screen.fill(pygame.color.THECOLORS['white'])
		for body in bodies:
			self.draw(body)
		pygame.display.flip()
		self.clock.tick(FPS)

	def draw(self, body):
		if isinstance(body, Circle):
			pygame.draw.circle(self.screen, pygame.color.THECOLORS['black'], \
				self.posToPygame(body.center), self.lengthToPygame(body.r))
		if isinstance(body, Rectangle):
			pygame.draw.polygon(self.screen, pygame.color.THECOLORS['black'], \
				map(self.posToPygame, body))

	def translate(self, vector):
		self.pos += vector

	def quit(self, event = None):
		pygame.quit()
		if event is None:
			sys.exit(0)
		sys.exit(pygame.event.event_name(event.type))

cam = Camera()
a = Rectangle(Vector2D(0,0), 1, 1, 0)
while 1:
	cam.update([a])