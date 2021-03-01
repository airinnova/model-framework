#!/usr/bin/env python3
# -*- coding: utf-8 -*-m

# _model.py
from mframework import FeatureSpec, ModelSpec

from ._run import run_model

# Here, we only have numerical user input. We only allow positive floats.
SCHEMA_POS_FLOAT = {'type': float, '>': 0}

# ===== MODEL =====
mspec = ModelSpec()

# Create the first feature 'ambiance'
fspec = FeatureSpec()
fspec.add_prop_spec('g', SCHEMA_POS_FLOAT, doc='Gravitational acceleration', max_items=1)
fspec.add_prop_spec('a', SCHEMA_POS_FLOAT, doc='Speed of sound', max_items=1)
mspec.add_feature_spec('ambiance', fspec, doc='Ambient flight conditions', max_items=1)

# Feature 'aerodynamics'
fspec = FeatureSpec()
fspec.add_prop_spec('CL', SCHEMA_POS_FLOAT, doc='Cruise lift coefficient', max_items=1)
fspec.add_prop_spec('CD', SCHEMA_POS_FLOAT, doc='Cruise drag coefficient', max_items=1)
fspec.add_prop_spec('Mach', SCHEMA_POS_FLOAT, doc='Cruise Mach number', max_items=1)
mspec.add_feature_spec('aerodynamics', fspec, doc='Aerodynamic properties', max_items=1)

# Feature 'propulsion'
fspec = FeatureSpec()
fspec.add_prop_spec('cT', SCHEMA_POS_FLOAT, doc='Thrust specific fuel consumption', max_items=1)
mspec.add_feature_spec('propulsion', fspec, doc='Profusion properties', max_items=1)

# Feature 'mass'
fspec = FeatureSpec()
fspec.add_prop_spec('m1', SCHEMA_POS_FLOAT, doc='Initial aircraft mass (at start of cruise)', max_items=1)
fspec.add_prop_spec('m2', SCHEMA_POS_FLOAT, doc='Final aircraft mass (at end of cruise)', max_items=1)
mspec.add_feature_spec('mass', fspec, doc='Mass properties', max_items=1)

# ===== RESULT =====
rspec = ModelSpec()

# Feature 'flight_mission'
fspec = FeatureSpec()
fspec.add_prop_spec('range', SCHEMA_POS_FLOAT, doc='Estimated range of the aircraft', max_items=1)
rspec.add_feature_spec('flight_mission', fspec, doc='Flight mission data', max_items=1)

mspec.results = rspec


class Model(mspec.user_class):
    def run(self):
        super().run()
        run_model(self)
