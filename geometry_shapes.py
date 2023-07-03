class Ellipsoid(object):
	"""# Ellipsoid
	x, y, z, a, b, c
	Optional scale factor: r
	Optional xy-angle: theta
	"""
	def __init__(self, x=0.0, y=0.0, z=0.0, a=1.0, b=1.0, c=1.0, r=1.0, theta=0):
		"""
		Initializes Ellipsoid
		"""
		self.x = x
		self.y = y
		self.z = z
		self.a = a
		self.b = b
		self.c = c
		self.r = r
		self.t = theta
	def move_and_scale(self, x=0.0, y=0.0, z=0.0, a=1.0, b=1.0, c=1.0, r=1.0, theta=0):
		"""
		Changes Ellipsoid
		"""
		self.x = x
		self.y = y
		self.z = z
		self.a = a
		self.b = b
		self.c = c
		self.r = r
		self.t = theta
	def check(self, x, y, z):
		"""
		Determines if [x,y,z] coordinate is inside of the ellipsoid
		"""
		from numpy import sin, cos
		return (((x-self.x) * cos(self.t) + (y-self.y) * sin(self.t))/self.a) ** 2.0 + (((y-self.y) * cos(self.t) - (x-self.x) * sin(self.t))/self.b) ** 2.0 + ((z-self.z)/self.c) ** 2.0 <= self.r ** 2.0
