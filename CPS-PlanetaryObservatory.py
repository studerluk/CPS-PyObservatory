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
	def __init__(self, x=0, y=0, z=0):
		self._x = x
		self._y = y
		self._z = z

	def __abs__(self):
		F = math.sqrt(pow(self._x,2) + pow(self._y,2) + pow(self._z,2))
		return F

	def __add__(self, other):
		x = self._x + other.getX()
		y = self._y + other.getY()
		z = self._z + other.getZ()
		return Vector(x, y, z)

	def __sub__(self, other):
		x = self._x - other.getX()
		y = self._y - other.getY()
		z = self._z - other.getZ()
		return Vector(x, y, z)

	def __mul__(self, other):
		x = self._x * other
		y = self._y * other
		z = self._z * other
		return Vector(x, y, z)

	def __truediv__(self, other):
		if not other == 0:
			x = self._x / other
			y = self._y / other
			z = self._z / other
			return Vector(x, y, z)
		else:
			raise

	def __str__(self):
		line = "%s | %s | %s" % (self._x, self._y, self._z)
		return line

	def __eq__(self, other):
		eqX = (self._x == other.getX())
		eqY = (self._y == other.getY())
		eqZ = (self._z == other.getZ())
		return (eqX and eqY and eqZ)

	def getX(self):
		return self._x

	def getY(self):
		return self._y

	def getZ(self):
		return self._z

class Universe:

	def __init__(self, id):
		window = turtle.Screen()
		window.colormode(255)

		if id == 0:
			sun = Planet("sun", Vector(0, 0), Vector(0, 0), 1000000, None)
			earth = Planet("earth", Vector(50, 0), Vector(0, 10), 10000, None)
			mars = Planet("mars", Vector(100, 0), Vector(0, 20), 10000, None)
			p1 = Planet("p1", Vector(155, 0), Vector(0, 7), 5000, None)
			p2 = Planet("p2", Vector(275, -50), Vector(0, 10), 200000, None)

			milky = SolarSystem()
			milky.addPlanet(sun)
			milky.addPlanet(earth)
			milky.addPlanet(mars)
			milky.addPlanet(p1)
			milky.addPlanet(p2)


		elif id == 1:
			milky = SolarSystem()
			sun = Planet("sun", Vector(), Vector(), 1000000, None)
			milky.addPlanet(sun)

			for i in range(25):
				pos = Vector(randint(-450, 450), randint(-450, 450), randint(-450, 450))
				v = Vector(randint(-10,10), randint(-10, 10), randint(-10,10))
				mass = randint(0, 1000)
				meteor = Planet("planet"+str(i), pos, v, mass, None)
				milky.addPlanet(meteor)


		elif id == 2:
			milky = SolarSystem()
			sun = Planet("sun", Vector(0, 0), Vector(0, 0), 1000000, None)
			milky.addPlanet(sun)

			for i in range(15):
				pos = Vector(i*30 + 30, 0)
				v = Vector(0, ((1)**i) * 10)
				mass = randint(0, 750)
				meteor = Planet("planet"+str(i), pos, v, mass, None)
				milky.addPlanet(meteor)


		elif id == 3:
			p1 = Planet("p1", Vector(100, -50), Vector(0, 15), 2000000, None)
			p2 = Planet("p2", Vector(-100, 50), Vector(0, -15), 2000000, None)

			milky = SolarSystem()
			milky.addPlanet(p1)
			milky.addPlanet(p2)

		for i in range(0, 10000):
			milky.tick()

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
			if not ("sun" in planet.name or "meteor" == planet.name[:-2]):
				planet.move()

		self.detectCollision()

# --- SolarSystem end ---

test = Universe(1)
