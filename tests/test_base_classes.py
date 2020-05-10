#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from mframework._mframework import _BaseSpec


def test_repr():

    class Spec(_BaseSpec):
        pass

    spec = Spec()
    spec.add_item_spec('a', int)
    spec.add_item_spec('b', int)

    assert repr(spec) == "<Specification for ('a', 'b')>"
