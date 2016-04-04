from math import sin, cos, radians, sqrt

class Vector2D(object):
	def __init__(self, x=0.0, y=0.0):
		self.x = x
		self.y = y

	@classmethod
	def from_list(cls, pos=(0,0)):
		return cls(pos[0], pos[1])

	@classmethod
	def from_angle(cls, angle=0.0, magnitude=1.0):
		return cls(cos(angle) * magnitude, sin(angle) * magnitude)

	def __getitem__(self, key):
		return (self.x, self.y)[key]

	def __setitem__(self, key, item):
		if key == 0:
			self.x = item
		elif key == 1:
			self.y = item
		else:
			if isinstance(key, slice):
				start = key.start
				stop  = key.stop
				step  = key.step

				if start is None:
					start = 0
				if stop is None:
					stop = 2
				if step is None:
					step = 1

				for e in xrange(start, stop, step):
					if e == 0:
						self.x = item[e]
					elif e == 1:
						self.y = item[e]
					else:
						raise IndexError, "Index %d out of range for " % e
			else:
				raise IndexError, "Index %d out of range for " % key

	def __add__(self, other):
		try:
			return Vector2D(self.x + other[0], self.y + other[1])
		except:
			return Vector2D(self.x + other, self.y + other)

	def __radd__(self, other):
		return self.__add__(other)

	def __sub__(self, other):
		try:
			return Vector2D(self.x - other[0], self.y - other[1])
		except:
			return Vector2D(self.x - other, self.y - other)

	def __rsub__(self, other):
		return self.__sub__(other)

	def __mul__(self, other):
		return Vector2D(self.x * other, self.y * other)

	def __rmul__(self, other):
		return self.__mul__(other)

	def __div__(self, other):
		return Vector2D(self.x / (other*1.0), self.y / (other*1.0))

	def __rdiv__(self, other):
		return self.__div__(other)

	def __repr__(self):
		return "(%.5f, %.5f)" % (self.x, self.y)

	def __nonzero__(self):
		return self.x or self.y

	def __iter__(self):
		return iter([self.x, self.y])

	def rotate_ip(self, angle):
		"""
		In place vector rotation
		Takes in angle as degrees
		"""
		angle %= 360
		if angle == 0.0:
			self.x, self.y = (self.x, self.y)
		elif angle == 90.0:
			self.x, self.y = (-self.y,self.x)
		elif angle == 180.0:
			self.x, self.y = (-self.x,-self.y)
		elif angle == 270.0:
			self.x, self.y = (self.y,-self.x)
		else:
			angle = radians(angle)
			sine = sin(angle)
			cosine = cos(angle)
			self.x, self.y = (cosine * self.x - sine * self.y,
							  sine * self.x + cosine * self.y)

	def rotate(self, angle):
		"""
		Produces new rotated vector
		Takes in angle as degrees from
		0 to 360
		"""
		angle %= 360
		if angle == 0.0:
			return Vector2D(self.x, self.y)
		elif angle == 90.0:
			return Vector2D(-self.y,self.x)
		elif angle == 180.0:
			return Vector2D(-self.x,-self.y)
		elif angle == 270.0:
			return Vector2D(self.y,-self.x)
		else:
			angle = radians(angle)
			sine = sin(angle)
			cosine = cos(angle)
			return self(cosine * self.x - sine * self.y,
							sine * self.x + cosine * self.y)

	def dot(self, other):
		return self.x*other[0] + self.y*other[1]

	def squared_magnitude(self):
		return self.x**2 + self.y**2

	def magnitude(self):
		return sqrt(self.x**2 + self.y**2)

	def normalize_ip(self):
		mag = self.magnitude()
		self.x /= mag
		self.y /= mag

	def normalize(self):
		mag = self.magnitude()
		return Vector2D(self.x / mag, self.y / mag)

class Line(object):
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

	def intersect(self, other):
		"""
		Returns point of intersection of two lines.
		Returns None if lines do not intersect.
		"""
		dx = (self.p1.x - self.p2.x, other.p1.x - other.p2.x)
		dy = (self.p1.y - self.p2.y, other.p1.y - other.p2.y)
		
		def det(a, b):
			return a[0] * b[1] - a[1] * b[0]

		div = det(dx, dy)
		if div == 0:
		   return None

		d = (det(self.p1, self.p2), det(other.p1, other.p2))
		x = det(d, dx) / float(div)
		y = det(d, dy) / float(div)
		return Vector2D(x, y)

	def intersect_fast(self, other):
		"""
		Returns True if lines intersect
		False otherwise
		http://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
		"""
		def on_seg(p, q, r):
			return (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
					q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y))

		def area(a, b, c):
			return ((b.x - a.x) * (c.y - a.y) -
					(c.x - a.x) * (b.y - a.y))

		o1 = area(self.p1, self.p2, other.p1)
		o2 = area(self.p1, self.p2, other.p2)
		o3 = area(other.p1, other.p2, self.p1)
		o4 = area(other.p1, other.p2, self.p2)

		return ((o1 != o2 and o3 != o4) or (o1 == 0 and on_seg(self.p1, other.p1, self.p2)) or
										   (o2 == 0 and on_seg(self.p1, other.p2, self.p2)) or
										   (o3 == 0 and on_seg(other.p1, self.p1, other.p2)) or
										   (o4 == 0 and on_seg(other.p1, self.p2, other.p2)))

class OBB2D(object):
	# Credit to:
	# http://www.flipcode.com/archives/2D_OBB_Intersection.shtml
	def __init__(self, center, w, h, angle):
		self.center = center
		self.w = w
		self.h = h

		self.update_angle(angle)

	def __getitem__(self, key):
		return self.p[key]

	def __iter__(self):
		return iter(self.p)

	def rotate(self, angle):
		self.update_angle(self.angle + angle)

	def translate(self, center):
		self.update_center(center+self.center)

	def update_size(self, w, h):
		self.w = w
		self.h = h

		self.update_axes()

	def update_angle(self, angle):
		self.angle = angle % 360

		angle = radians(angle)
		x = Vector2D( cos(angle), sin(angle))
		y = Vector2D(-sin(angle), cos(angle))

		x *= self.w / 2.0
		y *= self.h / 2.0

		self.p = [self.center - x - y,
				  self.center + x - y,
				  self.center + x + y,
				  self.center - x + y]

		self.update_axes()

	def update_center(self, center):
		translate = center - self.center
		for i in xrange(4):
			self.p[i] += translate

		self.center = center

	def update_axes(self):
		# axis are two edges of
		# the box extended from p[0]
		self.axis = [self.p[1] - self.p[0],
					 self.p[3] - self.p[0]]

		self.origin = [0,0]

		for i in xrange(2):
			self.axis[i] = self.axis[i] / (self.axis[i].squared_magnitude()*1.0)
			self.origin[i] = self.p[0].dot(self.axis[i])

	def overlaps(self, other):
		"""
		Helper function for
		intersects().
		"""
		for a in xrange(2):
			t = other.p[0].dot(self.axis[a])

			tmin = t
			tmax = t
			for c in xrange(1,4):
				t = other.p[c].dot(self.axis[a])

				if t < tmin:
					tmin = t
				if t > tmax:
					tmax = t

			if (tmin > 1+self.origin[a]) or (tmax < self.origin[a]):
				return False

		return True

	def intersects(self, other):
		"""
		Call this to check if two rectangles intersect.
		"""
		return self.overlaps(other) and other.overlaps(self)

def oo_collides(rect1, mask1, rect2, mask2):
	"""
	Collision
	between two objects.
	"""

def ro_collides(rect1, rect2, mask):
	"""
	Collision
	between an OBB and a
	pixel perfect object.
	"""

def rr_collides(rect1, rect2):
	"""
	Collision
	between two OBBs.
	"""
	return rect1.intersects(rect2)

def lo_collides(line, rect, mask):
	"""
	Collision
	between a line and a
	pixel perfect object.
	"""

def ll_collides(line1, line2):
	"""
	Collision
	between two lines.
	"""
	return line1.intersects(line2)

def lr_collides(line, rect):
	"""
	Collision
	between a line and an OBB.
	"""

def test():
	import pygame
	from constants import FPS

	pygame.init()
	screen = pygame.display.set_mode((600,400))
	clock = pygame.time.Clock()

	a = OBB2D(Vector2D(100,200), 100, 100, 0)
	b = OBB2D(Vector2D(200,300), 150, 100, 30)
	c = OBB2D(Vector2D(400,200), 100, 100, 90)

	font = pygame.font.SysFont("monospace", 30)

	frames = 0
	realfps = FPS
	while frames < 2400:
		def renderOBB(obb, screen):
			pygame.draw.lines(screen, (0,0,0), True, map(list,obb.p))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					b.update_size(b.w + 2, b.h + 2)
				if event.button == 5:
					b.update_size(b.w - 2, b.h - 2)

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

		pygame.display.flip()
		clock.tick(FPS)
		realfps = clock.get_fps()
		if realfps == 0:
			realfps = FPS
		frames += 1

	pygame.quit()

if __name__=='__main__':
	test()