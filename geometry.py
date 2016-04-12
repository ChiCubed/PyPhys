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
from constants import FPS

WORLD_DENSITY = 1.204 # Air in kg/m^3, used as kg/m^2. Temporary

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