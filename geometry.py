# geometry.py - Defines physics objects.
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

from math import sqrt
from util import *
from constants import PIXELS_PER_METRE, WORLD_DENSITY, GRAVITY, FPS

class Circle(object):
	def __init__(self, center, r, dynamic=True):
		self.center = center
		self.r = r
		self.rs = self.r**2
		self.dynamic = dynamic

		self.velocity = Vector2D(0,0)

	@classmethod
	def from_points(self, p1, p2, dynamic = True):
		self.__init__(p1, (p2 - p1).magnitude())

	@classmethod
	def from_squaredradius(self, center, rs, dynamic = True):
		self.center = center
		self.r = sqrt(rs)
		self.rs = rs

	def scale(self, scale):
		self.update_radius(self.radius * scale)

	def update_radius(self, radius):
		self.r = radius
		self.rs = self.r**2

	def translate(self, vector):
		self.update_center(self.center + vectorE)

	def update_center(self, center):
		self.center = center

	def intersects(self, other):
		"""
		Check if this circle intersects another circle.
		"""
		if not isinstance(other, Circle):
			raise TypeError("Circle can only be intersected with another Circle. Try one of the helper functions i.e. xx_collides.")
		return (other.center - self.center).squared_magnitude() <= (self.rs + other.rs)

	def apply_impulse(self, impulse):
		if not self.dynamic:
			return
		self.velocity += impulse

	def update_physics(self):
		if not self.dynamic:
			return
		self.translate(self.velocity)

class Rectangle(OBB2D):
	def __init__(self, center, w, h, angle = 0, mass = 1, dynamic = True):
		super(Rectangle, self).__init__(center, w, h, angle)
		self.dynamic = dynamic

		self.mass = mass # kg
		self.calculate_density()

		self.velocity = Vector2D(0,0) # m/s

	def calculate_density(self):
		# Calculates density
		# in kg / m^2
		self.density = self.mass / (self.w * self.h)
		print self.density

	def calculate_drag(self):
		# Drag coefficient of box:
		# Assumed to be 1.05,
		# which is close enough
		# for pretty much any
		# intent and purpose
		Cd      = 1.05

		# Accurate enough
		area    = (self.w + self.h) / 2
		density = WORLD_DENSITY

		return Cd * density * self.velocity.squared_magnitude() * area * 0.5

	def apply_impulse(self, impulse):
		if not self.dynamic:
			return
		# Impulse = m (v-u)
		# v-u = Impulse / m
		# v = (Impulse / m) + u
		# where u is starting
		# velocity
		self.velocity += (impulse / self.mass)

	def update_physics(self):
		if not self.dynamic:
			return
		self.translate(self.velocity)

		drag = self.calculate_drag()
		# Note: F = ma
		# so drag = mass * acceleration
		# so acceleration = drag / mass

		acceleration = 0 # GRAVITY / FPS
		self.velocity += acceleration
		self.velocity *= 0.9 # Temporary drag hack
		# acceleration = Vector2D.from_angle(self.velocity.angle(), -drag / self.mass)
		# self.velocity += acceleration

class OneWayPlatform(object):
	def __init__(self, p1, p2, dynamic=False):
		self.line = Line(p1, p2)
		self.dynamic = dynamic
		self.update_normal()

	def check_collision(self, rect, mask=None):
		collides = False
		if mask is None:
			collides = ro_collides(self.line, rect, mask)
		if lo_collides(self, rect, mask):
			pass # TODO

	def update_normal(self):
		self.normal = self.angle.rotated(90)
		self.normal.normalize_ip()

def test():
	import pygame
	from constants import FPS

	pygame.init()
	screen = pygame.display.set_mode((800,600))
	clock = pygame.time.Clock()

	a = Rectangle(Vector2D(1,2), 1, 1, 0)

	font = pygame.font.SysFont("monospace", 30)

	duration = 60 * FPS

	frames = 0
	realfps = FPS
	while frames < duration:
		def renderOBB(obb, screen):
			pygame.draw.polygon(screen, (0,0,0), map(list, map(lambda x: Vector2D(2*x.x*PIXELS_PER_METRE,600) - (x * PIXELS_PER_METRE), obb)))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return

		screen.fill((255,255,255))

		renderOBB(a, screen)
		
		if pygame.mouse.get_pressed()[0]:
			pos = (Vector2D(2*pygame.mouse.get_pos()[0],600) - Vector2D.from_list(pygame.mouse.get_pos())) / PIXELS_PER_METRE
			a.apply_impulse((pos - a.center)/20)
		a.update_physics()

		text = font.render(str(duration-frames), True, (0,0,0))
		screen.blit(text, [0,0])

		pygame.display.flip()
		clock.tick(FPS)
		realfps = clock.get_fps()
		if realfps == 0:
			realfps = FPS
		frames += 1

	pygame.quit()

if __name__ == '__main__':
	test()
