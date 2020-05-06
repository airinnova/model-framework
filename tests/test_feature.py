#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mframework import FeatureSpec


def test_basic():
    """
    Test basic functionality of 'FeatureSpec'
    """
    print()

    # ===== Specifications =====

    fspec = FeatureSpec()
    fspec.add_prop_spec('A', int)
    fspec.add_prop_spec('B', int)
    fspec.add_prop_spec('C', int, singleton=False)
    fspec.add_prop_spec('D', {'type': int, '>': 0})

    # Check that schemas cannot be defined twice
    with pytest.raises(KeyError):
        fspec.add_prop_spec('D', str)

    Feature = fspec.provide_user_class()
    f = Feature()

    # ===== User logic =====

    # ----- set() method -----
    f.set('A', 5)
    f.set('B', 8)
    f.set('B', 9)

    # Check the added values
    assert f.get('A') == 5
    assert f.get('B') == 9

    # Property 'B' can only have one entry
    assert f.len('B') == 1

    # Check that keys which are not allowed cannot be set
    with pytest.raises(KeyError):
        f.set("PROPERTY_DOES_NOT_EXIST", 10)

    # Value for 'D' can only be positive (see specification)
    f.set('D', 4)
    with pytest.raises(ValueError):
        f.set('D', -4)

    # ----- add() method -----
    f.add('C', 11)
    f.add('C', 22)
    f.add('C', 33)

    # Property 'C' has three entries
    assert f.len('C') == 3

    # Check that keys which are not allowed cannot be added
    with pytest.raises(KeyError):
        f.add("PROPERTY_DOES_NOT_EXIST", 10)

    # Check the added values
    assert f.get('C') == [11, 22, 33]

    exp_items = [11, 22, 33]
    for i, item in enumerate(f.iter('C')):
        assert item == exp_items[i]

    # Cannot iterate over unique property
    with pytest.raises(KeyError):
        for _ in f.iter('A'):
            pass


def test_complex_schema():
    """
    Test variations of more complex property schemas
    """
    print()

    # ===== Specifications =====

    schema_global = {
        'name': {'type': str, 'min_len': 1},
        'mass': {'type': float, '>': 0},
    }

    schema_wing = {
        'id': {'type': str, 'min_len': 3},
        'span': {'type': float, '>': 0},
        'area': {'type': float, '>': 0},
    }

    fspec_aircraft = FeatureSpec()
    fspec_aircraft.add_prop_spec('global', schema_global)
    fspec_aircraft.add_prop_spec('wing', schema_wing, singleton=False)

    Aircraft = fspec_aircraft.provide_user_class()
    aircraft = Aircraft()

    # ===== User logic =====

    aircraft.set('global', {'name': 'AD42', 'mass': 50e3})

    aircraft.add('wing', {'id': 'MainWing', 'span': 32.4, 'area': 55.0})
    aircraft.add('wing', {'id': 'HorizTail', 'span': 7.5, 'area': 18.2})

    # Overwrite 'global'
    aircraft.set('global', {'name': 'AD8888', 'mass': 49.9e3})

    # Add method does not apply to 'global'
    with pytest.raises(RuntimeError):
        aircraft.add('global', {'name': 'abc', 'mass': 1.0})

    # Set method does not apply to 'wing'
    with pytest.raises(RuntimeError):
        aircraft.set('wing', {'id': 'abc', 'span': 1.0, 'area': 1.0})

    # Cause schemadict error
    with pytest.raises(TypeError):
        aircraft.set('wing', {'id': 'abc', 'span': 'WRONG_VALUE', 'area': 1.0})


# def test_repr():
#     fspec = FeatureSpec()
#     fspec.add_prop_spec('x', int)
#     Feature = fspec.provide_user_class()

#     f = Feature()
#     assert 'feature' in repr(f).lower()
#     assert 'parent' in repr(f).lower()
