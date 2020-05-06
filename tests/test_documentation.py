#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mframework import FeatureSpec, ModelSpec


def test_feature_doc():
    fspec = FeatureSpec()
    fspec.add_prop_spec('E', {'type': float, '>': 0}, doc="Young's modulus")
    fspec.add_prop_spec('A', {'type': float, '>': 0}, doc="Area")
    docs = fspec.get_docs()

    assert len(docs) == 2
    assert docs['E']['main'] == "Young's modulus"
    assert docs['A']['main'] == "Area"

    assert docs['E']['sub'] is None
    assert docs['A']['sub'] is None


def test_model_doc():
    cross_section = FeatureSpec()
    cross_section.add_prop_spec('E', {'type': float, '>': 0}, doc="Young's modulus")
    cross_section.add_prop_spec('A', {'type': float, '>': 0}, doc="Area")

    geom = FeatureSpec()
    geom.add_prop_spec('point1', list, doc="Coordinates of point 1")
    geom.add_prop_spec('point2', list, doc="Coordinates of point 2")

    mspec = ModelSpec()
    mspec.add_feature_spec('CrossSection', cross_section, doc="Beam cross section")
    mspec.add_feature_spec('Geom', geom, doc="Beam geometry")

    docs = mspec.get_docs()

    assert docs['CrossSection']['main'] == "Beam cross section"
    assert docs['Geom']['main'] == "Beam geometry"

    assert docs['CrossSection']['sub']['E']['main'] == "Young's modulus"
    assert docs['CrossSection']['sub']['A']['main'] == "Area"
    assert docs['Geom']['sub']['point1']['main'] == "Coordinates of point 1"
    assert docs['Geom']['sub']['point2']['main'] == "Coordinates of point 2"
