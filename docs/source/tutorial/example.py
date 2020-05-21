#!/usr/bin/env python3
# -*- coding: utf-8 -*-m

from aircraft import Model

# First, we create a new aircraft model instance
ac = Model()

# In our case the aircraft model, will have the feature 'aerodynamics'.
# Below, we first create an instance of this feature, and subsequently
# we assign numerical values to the aerodynamic properties.
aero = ac.set_feature('aerodynamics')
aero.set('CL', 1.5)
aero.set('CD', 0.08)
aero.set('Mach', 0.8)

# Our aircraft model also has a 'ambiance' feature to set the gravitational
# acceleration and speed of sound.
amb = ac.set_feature('ambiance')
amb.set('g', 9.8)
amb.set('a', 300.0)

# We can set the thrust specific fuel consumption in the feature 'propulsion'
prop = ac.set_feature('propulsion')
prop.set('cT', 20e-6)

# Finally, we have a feature called 'mass' where we assign initial and final
# masses
mass = ac.set_feature('mass')
mass.set('m1', 70e3)

# Once, we have set up the model we can call the 'run()' method which
# will compute the range for both configurations and print the results.
for m2 in range(35, 61, 5):
    mass.set('m2', m2*1e3)
    ac.run()
