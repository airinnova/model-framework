#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test errors for user classes
"""

import pytest

from mframework import FeatureSpec, ModelSpec


def test_set_feature():
    """

    """
    print()

    fspec = FeatureSpec()
    mspec = ModelSpec()

    fspec.add_prop_spec('a', int, singleton=True)
    fspec.add_prop_spec('b', int, singleton=False)
    mspec.add_feature_spec('A', fspec, singleton=True)

    fspec.add_prop_spec('1', str, singleton=True)
    fspec.add_prop_spec('2', str, singleton=False)
    mspec.add_feature_spec('B', fspec, singleton=False)

    m = mspec.provide_user_class()()

    # Feature 'A' is non-singleton
    with pytest.raises(RuntimeError):
        m.add_feature('A')
    m.set_feature('A')

    # Feature 'B' is singleton
    with pytest.raises(RuntimeError):
        m.set_feature('B')
    m.add_feature('B')
    m.add_feature('B')
    m.add_feature('B')

    fa = m.get('A')
    fa.set('a', 2)

    fb = m.get('B')
    assert len(fb) == 3

    with pytest.raises(KeyError):
        for _ in m.iter('A'):
            pass

    for _ in m.iter('B'):
        pass
