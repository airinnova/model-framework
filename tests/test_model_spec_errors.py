#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test errors for user classes
"""

import pytest

from mframework import FeatureSpec, ModelSpec


def test_add_feature_spec():
    """
    Test 'add_feature_spec()' method
    """

    fspec_door = FeatureSpec()
    fspec_door.add_prop_spec('color', str)

    fspec_motor = FeatureSpec()
    fspec_motor.add_prop_spec('type', str)

    mspec_car = ModelSpec()

    # ----- Wrong type: key -----
    with pytest.raises(TypeError):
        mspec_car.add_feature_spec(22, fspec_door)

    # ----- Wrong type: feature_spec -----
    with pytest.raises(TypeError):
        mspec_car.add_feature_spec('door', fspec_door.provide_user_class())

    with pytest.raises(TypeError):
        mspec_car.add_feature_spec('door', fspec_door.provide_user_class()())

    # ----- Wrong type: singleton -----
    with pytest.raises(TypeError):
        mspec_car.add_feature_spec('door', fspec_door, singleton='yes')

    # Cannot add property twice...
    mspec_car.add_feature_spec('motor', fspec_motor)
    with pytest.raises(KeyError):
        mspec_car.add_feature_spec('motor', fspec_motor)
