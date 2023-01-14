# planets.py

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D


class SolarSystem():
	"""This class creates the SolarSystem object."""
	def __init__(selfs):
		"""With selfs you can access private atributes of the object.
		"""
		selfs.size = 1000
		selfs.planets = []
		# This initializes the 3D figure
		selfs.fig = plt.figure()
		selfs.ax = Axes3D(selfs.fig, auto_add_to_figure=False)
		selfs.fig.add_axes(selfs.ax)
		selfs.dT = 1

	def add_planet(selfs, planet):
		"""Every time a planet is created it gets put into the array."""
		selfs.planets.append(planet)

	def update_planets(selfs):
		""" This method moves and draws all of the planets . """
		selfs.ax.clear()
		for planet in selfs.planets:
			planet.move()
			planet.draw()

	def fix_axes(selfs):
		"""The axes would change with each iteration otherwise."""
		selfs.ax.set_xlim((-selfs.size/2, selfs.size/2))
		selfs.ax.set_ylim((-selfs.size/2, selfs.size/2))
		selfs.ax.set_zlim((-selfs.size/2, selfs.size /2))

	def gravity_planets(selfs):
		""" This method calculated gravity interaction for every planet."""
		for i, first in enumerate(selfs.planets):
			for second in selfs.planets[i+1:]:
				first.gravity(second)

class Planet():
	""" This class creates the Planet object . """
	def __init__ (
		selfs,
		SolarSys,
		mass,
		position=(0, 0, 0),
		velocity=(0, 0, 0)
	):
		selfs.SolarSys = SolarSys
		selfs.mass = mass
		selfs.position = position
		selfs.velocity = velocity
		# The planet is automatically added to the SolarSys.
		selfs.SolarSys.add_planet(selfs)
		selfs.color = "black"

	def move(selfs):
		""" The planet is moved based on the velocity . """
		selfs.position = (
			selfs.position[0]+selfs.velocity[0]*SolarSys.dT,
			selfs.position[1]+selfs.velocity[1]*SolarSys.dT,
			selfs.position[2]+selfs.velocity[2]*SolarSys.dT
		)

	def draw(selfs):
		""" The method to draw the planet . """
		selfs.SolarSys.ax.plot(
			*selfs.position,
			marker="o",
			markersize=10 ,
			color=selfs.color
		)

	def gravity(selfs, other):
		""" The method to compute gravitational force for two
		planets . numpy module is used to handle vectors .
		"""
		distance = np.subtract(other.position, selfs.position)
		distanceMag = np.linalg.norm(distance)
		distanceUnit = np.divide(distance, distanceMag)
		forceMag = selfs.mass*other.mass / (distanceMag**2)
		force = np.multiply(distanceUnit, forceMag)
		# Switch makes force on selfs opossite to other
		switch = 1
		for body in selfs, other:
			acceleration = np.divide(force, body.mass)
			acceleration = np.multiply(force, SolarSys.dT*switch)
			body.velocity = np.add(body.velocity, acceleration)
			switch *= -1


class Sun(Planet):
	""" This class is inherited from Planet . Everything is
	the same as in planet , except that the position of the
	sun is fixed . Also , the color is yellow .
	"""
	def __init__(
		selfs,
		SolarSys,
		mass=10000,
		position=(0, 0, 0),
		velocity=(0, 0, 0)
	):
		super(Sun, selfs).__init__(SolarSys, mass, position, velocity)
		selfs.color = "yellow"

	def move(selfs):
		selfs.position = selfs.position


# Instantiating of the solar system.
SolarSys = SolarSystem()

# Instantiating of planets.
earth = Planet(SolarSys, mass=1, position=(149.6,149.6,149.6), velocity=(29.8,29.8,29.8))
mercury = Planet(SolarSys, mass=0.0553, position=(57.9,57.9,57.9), velocity=(47.9,47.9,47.9))
venus = Planet(SolarSys, mass=0.815, position=(108.2,108.2,108.2), velocity=(35,35,35))
mars = Planet(SolarSys, mass=0.107, position=(228,228,228), velocity=(24.1,24.1,24.1))
jupiter = Planet(SolarSys, mass=317.8, position=(778.5,778.5,778.5), velocity=(13.1,13.1,13.1))
saturn = Planet(SolarSys, mass=95.2, position=(1432,1432,1432), velocity=(9.7,9.7,9.7))
uranus = Planet(SolarSys, mass=14.5, position=(2867,2867,2867), velocity=(6.8,6.8,6.8))
neptune = Planet(SolarSys, mass=17.1, position=(4515,4515,4515), velocity=(5.4,5.4,5.4))

# Instantiating of the sun.
sun = Sun(SolarSys)


def animate(i):
	""" This controls the animation. """
	print("The frame is:", i)
	SolarSys.gravity_planets()
	SolarSys.update_planets()
	SolarSys.fix_axes()

# This calls the animate function and creates animation.
anim = animation.FuncAnimation(SolarSys.fig, animate, frames=100, interval=100)
# This prepares the writer for the animation.
writervideo = animation.FFMpegWriter(fps=60)
# This saves the animation.
anim.save("planets_animation.mp4", writer=writervideo, dpi=200)