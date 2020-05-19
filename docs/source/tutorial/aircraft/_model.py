#!/usr/bin/env python3
# -*- coding: utf-8 -*-m

from mframework import FeatureSpec, ModelSpec

from ._run import run_model

# ===== MODEL =====
mspec = ModelSpec()

fspec = FeatureSpec()
fspec.add_prop_spec('CL', {'type': float, '>': 0})
fspec.add_prop_spec('CD', {'type': float, '>': 0})
fspec.add_prop_spec('Mach', {'type': float, '>': 0})
mspec.add_feature_spec('aerodynamics', fspec, doc='TODO')

fspec = FeatureSpec()
fspec.add_prop_spec('cT', {'type': float, '>': 0})
mspec.add_feature_spec('propulsion', fspec, doc='TODO')

fspec = FeatureSpec()
fspec.add_prop_spec('m1', {'type': int, '>': 0})
fspec.add_prop_spec('m2', {'type': int, '>': 0})
mspec.add_feature_spec('mass', fspec, doc='TODO')

# ===== RESULT =====
rspec = ModelSpec()

fspec = FeatureSpec()
fspec.add_prop_spec('range', {'type': float, '>': 0})
rspec.add_feature_spec('flight_mission', fspec)

mspec.results = rspec


class Model(mspec.user_class):
    def run(self):
        super().__init__()
        run_model(self)
