import turtle, math
from random import randint

#SUN_MASS = 1.98855 * 10 ** 30			# kg
#EARTH_MAX_DISTANCE = 150000000000		# m
#EARTH_MASS = 5.97219 * 10 ** 24			# kg
#EARTH_SPEED = 29780						# m/s

# to use / and * with vectors and scalars use as follows
# Vector / scalar
# Vector * scalar
# other way around does not work
class Vector:
	def __init__(self, x=0, y=0):
		self._x = x
		self._y = y

	def __abs__(self):
		F = math.sqrt(pow(self._x,2) + pow(self._y,2))
		return F

	def __add__(self, other):
		x = self._x + other.getX()
		y = self._y + other.getY()
		return Vector(x, y)

	def __sub__(self, other):
		x = self._x - other.getX()
		y = self._y - other.getY()
		return Vector(x, y)

	def __mul__(self, other):
		x = self._x * other
		y = self._y * other
		return Vector(x,y)

	def __truediv__(self, other):
		if not other == 0:
			x = self._x / other
			y = self._y / other
			return Vector(x,y)
		else:
			raise

	def __str__(self):
		line = str(self._x) + "|" + str(self._y)
		return line

	def __eq__(self, other):
		eqX = (self._x == other.getX())
		eqY = (self._y == other.getY())
		# eqF = (abs(self) == abs(other))
		# return (eqX and eqY and eqF)
		return (eqX and eqY)

	def getX(self):
		return self._x

	def getY(self):
		return self._y

class Universe:

	def __init__(self):
		window = turtle.Screen()
		window.colormode(255)

		"""
		sun = Planet("sun", Vector(0, 0), Vector(0, 0), 1000000, None)
		earth = Planet("earth", Vector(50, 0), Vector(0, 10), 10000, None)
		mars = Planet("mars", Vector(100, 0), Vector(0, 20), 10000, None)
		p1 = Planet("p1", Vector(155, 0), Vector(0, 7), 1000, None)
		p2 = Planet("p2", Vector(275, 0), Vector(0, -20), 100000, None)

		milky = SolarSystem()
		milky.addPlanet(sun)
		milky.addPlanet(earth)
		milky.addPlanet(mars)
		milky.addPlanet(p1)
		milky.addPlanet(p2)
		"""

		milky = SolarSystem()
		sun = Planet("sun", Vector(0, 0), Vector(0, 0), 1000000, None)
		milky.addPlanet(sun)

		for i in range(15):
			pos = Vector(randint(-450, 450), randint(-450, 450))
			v = Vector(randint(-10,10), randint(-10, 10))
			mass = randint(0, 750)
			meteor = Planet("planet"+str(i), pos, v, mass, None)
			milky.addPlanet(meteor)

		"""
		milky = SolarSystem()
		sun = Planet("sun", Vector(0, 0), Vector(0, 0), 1000000, None)
		milky.addPlanet(sun)

		for i in range(15):
			pos = Vector(i*20 + 20, 0)
			v = Vector(0, 10)
			mass = randint(0, 750)
			meteor = Planet("planet"+str(i), pos, v, mass, None)
			milky.addPlanet(meteor)
		"""


		"""
		p1 = Planet("p1", Vector(100, -50), Vector(0, 15), 2000000, None)
		p2 = Planet("p2", Vector(-100, 50), Vector(0, -15), 2000000, None)

		milky = SolarSystem()
		milky.addPlanet(p1)
		milky.addPlanet(p2)
		"""

		for i in range(0, 10000):
			milky.tick()
			#print("-----")

		turtle.getscreen()._root.mainloop()

# --- Universe end ---

class Planet:

	def __init__(self, name, pos, v, mass, color=None):
		self.pos = pos
		self.v = v
		self.mass = mass

		# size: radius in meter
		self.size = math.log(mass)/math.log(1000)

		self.name = name

		self.line = turtle.Turtle()
		self.line.hideturtle()
		self.line.speed(1000)
		self.line.shape("circle")
		self.line.shapesize(self.size)

		if not color:
			color = [randint(0,255), randint(0,255), randint(0,255)]

		self.line.color(color[0], color[1], color[2])
		self.line.penup()
		self.line.setpos(pos.getX(), pos.getY())
		self.line.pendown()
		self.line.showturtle()

		#print(self.name+" initialized: pos: "+str(self.pos)+" v: "+str(self.v)+" mass: "+str(self.mass))

	def move(self):
		self.pos += self.v
		self.line.setpos(self.pos.getX(), self.pos.getY())

		#print("Pos: " + self.name + ": " + str(self.pos))

	def __eq__(self, other):
		return self.name == other.name

	def destroy(self):
		self.line.penup()
		self.line.hideturtle()

# --- Planet end ---

# Gravities are calculated as follows:
# r = (Rx^2 + Ry^2) ^ 0.5
# F = G * (m1 * m2) / r
# F = m * a -> a = F / m
# F = k * r -> k = F / r
# ax = Rx * k / m
# ay = Ry * k / m

class SolarSystem:
	# G_CONST = 66.7384 * pow(10, -12);
	G_CONST = pow(10, -4);

	def __init__(self, debug = False):
		self.planets = []
		self.debug = debug


	def addPlanet(self, planet):
		self.planets.append(planet)

	# U = (m1*v1 + m2*v2)/(m1+m2)
	def detectCollision(self):
		otherPlanets = self.planets
		collisionPairs = []
		for planet in self.planets:
			otherPlanets = list(filter((planet).__ne__, otherPlanets))
			for otherPlanet in otherPlanets:
				if planet == otherPlanet: continue

				R = planet.pos - otherPlanet.pos
				distance = abs(R)

				# the *10 is because the size actually is 10x the size provided
				#print("Testing %s and %s" % (planet.name, otherPlanet.name))
				if (distance <= (planet.size*10 + otherPlanet.size*10)):
					collisionPairs.append([planet, otherPlanet])

		for pair in collisionPairs:
			totalMass = pair[0].mass + pair[1].mass

			u = (pair[0].v * pair[0].mass + pair[1].v * pair[1].mass) / totalMass

			pos = pair[1].pos + (pair[0].pos - pair[1].pos) / 2

			newPlanet = Planet(pair[0].name+'-'+pair[1].name, pos, u, totalMass, None)

			for planet in pair:
				planet.destroy()
				self.planets = list(filter((planet).__ne__, self.planets))
			self.addPlanet(newPlanet)

	def calcGravity(self, planet):
		objects = self.planets
		for obj in objects:
			if (obj != planet):
				R = obj.pos - planet.pos
				r = abs(R)

				F = self.G_CONST * ((obj.mass * planet.mass) / r)
				k = F / r

				planet.v += (R * k) / planet.mass


	def tick(self):
		system = self.planets

		for planet in system:
			self.calcGravity(planet)

		for planet in system:
			self.detectCollision()
			if not ("sun" in planet.name or "meteor" == planet.name[:-2]):
				planet.move()

# --- SolarSystem end ---

test = Universe()
