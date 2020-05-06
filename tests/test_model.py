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


def test_from_dict():
    fspec1 = FeatureSpec()
    fspec1.add_prop_spec('a', int)
    fspec1.add_prop_spec('b', str)
    fspec1.add_prop_spec('c', {'type': bool})

    fspec2 = FeatureSpec()
    fspec2.add_prop_spec('one', int)
    fspec2.add_prop_spec('two', str)
    fspec2.add_prop_spec('three', {'type': bool})

    mspec = ModelSpec()
    mspec.add_feature_spec('A', fspec1)
    mspec.add_feature_spec('B', fspec2)
    Model = mspec.provide_user_class()

    props1 = {
        'a': 42,
        'b': 'snake',
        'c': True,
    }

    props2 = {
        'one': 43,
        'two': 'Snake',
        'three': False,
    }

    model_dict = {
        'A': props1,
        'B': props2,
    }

    m = Model().from_dict(model_dict)
    m_fa = m.get('A')
    m_fb = m.get('B')

    assert m_fa.get('a') == 42
    assert m_fa.get('b') == 'snake'
    assert m_fa.get('c') is True

    assert m_fb.get('one') == 43
    assert m_fb.get('two') == 'Snake'
    assert m_fb.get('three') is False

# def test_repr():
#     fspec = FeatureSpec()
#     fspec.add_prop_spec('x', int)

#     mspec = ModelSpec()
#     mspec.add_feature_spec('X', fspec)

#     m = mspec.provide_user_class()()

#     assert 'model' in repr(m).lower()
