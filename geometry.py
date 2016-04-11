from math import sqrt
from util import *

class Circle(object):
	def __init__(self, center, r, dynamic=True):
		self.center = center
		self.r = r
		self.rs = r**2
		self.dynamic = dynamic

		self.velocity = Vector2D(0,0)

	@classmethod
	def from_points(self, p1, p2, dynamic = True):
		self.__init__(p1, (p2 - p1).magnitude())

	@classmethod
	def from_squaredradius(self, center, rs, dynamic = True):
		self.center = center
		self.r = sqrt(r)
		self.rs = rs

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
		self.center += velocity

class Rectangle(OBB2D):
	def __init__(self, center, w, h, angle = 0, dynamic = True):
		super(Rectangle, self).__init__(center, w, h, angle)
		self.dynamic = dynamic

		self.velocity = Vector2D(0,0)

	def apply_impulse(self, impulse):
		if not self.dynamic:
			return
		self.velocity += impulse

	def update_physics(self):
		if not self.dynamic:
			return
		self.center += velocity

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
	screen = pygame.display.set_mode((600,400))
	clock = pygame.time.Clock()

	a = Rectangle(Vector2D(100,200), 50, 50, 0)

	font = pygame.font.SysFont("monospace", 30)

	duration = 20 * FPS

	frames = 0
	realfps = FPS
	while frames < duration:
		def renderOBB(obb, screen):
			pygame.draw.lines(screen, (0,0,0), True, map(list,obb))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					b.scale(1.1)
				if event.button == 5:
					b.scale(1/1.1)

		screen.fill((255,255,255))


		renderOBB(a, screen)
		renderOBB(b, screen)
		renderOBB(c, screen)
		
		b.rotate(6.0/realfps)
		b.update_center(Vector2D.from_list(pygame.mouse.get_pos()))

		text = font.render(str(rr_collides(a,b)), True, (0,0,0))
		screen.blit(text, [600/2-text.get_rect().width/2, 50])

		text = font.render(str(rr_collides(b,c)), True, (0,0,0))
		screen.blit(text, [600/2-text.get_rect().width/2, 100])

		text = font.render(str(duration-frames), True, (0,0,0))
		screen.blit(text, [0,0])

		pygame.display.flip()
		clock.tick(FPS)
		realfps = clock.get_fps()
		if realfps == 0:
			realfps = FPS
		print realfps
		frames += 1

	pygame.quit()

if __name__ == 'main':
	test()
