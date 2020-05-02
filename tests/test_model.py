#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mframework import FeatureSpec, ModelSpec


def test_basic():
    """
    Test basic functionality of 'ModelSpec'
    """
    print()

    # ===== Specifications =====

    fspec_beam = FeatureSpec()
    fspec_beam.add_prop_spec('A', int)
    fspec_beam.add_prop_spec('B', int, singleton=False)

    fspec_study = FeatureSpec()
    fspec_study.add_prop_spec('static', bool)

    mspec = ModelSpec()
    mspec.add_feature_spec('beam', fspec_beam, singleton=False)
    mspec.add_feature_spec('study', fspec_study, singleton=True)

    Model = mspec.provide_user_class()
    beam_model = Model()

    # ===== User logic =====

    beam1 = beam_model.add_feature('beam')
    beam1.set('A', 1)
    beam1.add('B', 2)
    beam1.add('B', 3)

    beam2 = beam_model.add_feature('beam')
    beam2.set('A', 2)
    beam2.add('B', 4)
    beam2.add('B', 6)

    study = beam_model.set_feature('study')
    study.set('static', True)

    # Beam 1 and 2 have different values for the same property
    assert beam1.get('A') == 1
    assert beam2.get('A') == 2

    # Beams are different, but the parent specification is the same
    assert beam1.uid != beam2.uid
    assert beam1._parent_uid == beam2._parent_uid
