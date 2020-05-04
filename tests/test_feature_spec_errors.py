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


def test_f_provide_user_class():
    """
    Test method 'provide_user_class()'
    """
    print()

    fspec = FeatureSpec()
    fspec.add_prop_spec('a', int, singleton=True)
    fspec.add_prop_spec('b', int, singleton=False)
    Feature = fspec.provide_user_class()

    f = Feature()
    f.set('a', 12)
    f.add_many('b', (11, 22, 33))

    with pytest.raises(KeyError):
        f.set('x', 55)

    with pytest.raises(RuntimeError):
        f.add('a', 55)

    with pytest.raises(RuntimeError):
        f.set('b', 55)

    assert f.len('a') == 1
    assert f.len('b') == 3
    assert f.get('a') == 12
    assert f.get('b') == [11, 22, 33]
