#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test errors for specification classes
"""

import pytest

from mframework import FeatureSpec, ModelSpec


def test_f_add_property_spec():
    """
    Test method 'add_prop_spec()'
    """

    fspec = FeatureSpec()

    # ----- Wrong type: key -----
    with pytest.raises(TypeError):
        fspec.add_prop_spec(44, int)

    # ----- Wrong type: schema -----
    class MySpecialNumber:
        pass
    with pytest.raises(TypeError):
        fspec.add_prop_spec('number', MySpecialNumber)

    # ----- Wrong type: singleton -----
    with pytest.raises(TypeError):
        fspec.add_prop_spec('number', int, singleton='yes')

    # ----- Wrong type: required -----
    with pytest.raises(TypeError):
        fspec.add_prop_spec('number', int, singleton=True, required='yes')

    # Cannot add property twice...
    fspec.add_prop_spec('color', str)
    with pytest.raises(KeyError):
        fspec.add_prop_spec('color', str)
