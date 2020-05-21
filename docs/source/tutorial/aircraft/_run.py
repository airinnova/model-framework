#!/usr/bin/env python3
# -*- coding: utf-8 -*-m

# _run.py
from math import log


def run_model(model):
    """Run the full model analysis"""

    # Compute the aircraft range
    breguet_range(model)

    m1 = model.get('mass').get('m1')
    m2 = model.get('mass').get('m2')
    r = model.results.get('flight_mission').get('range')
    print(f"Range: {r/1000:7.1f} km (m1: {m1/1e3:.1f} t | m2: {m2/1e3:.1f} t)")


def breguet_range(model):
    """Estimate the range"""

    M = model.get('aerodynamics').get('Mach')
    cD = model.get('aerodynamics').get('CD')
    cL = model.get('aerodynamics').get('CL')

    a = model.get('ambiance').get('a')
    g = model.get('ambiance').get('g')

    cT = model.get('propulsion').get('cT')

    m1 = model.get('mass').get('m1')
    m2 = model.get('mass').get('m2')

    # Solve Breguet equation
    r = a*M*cL*log(m1/m2)/(g*cT*cD)

    fm = model.results.set_feature('flight_mission')
    fm.set('range', r)
