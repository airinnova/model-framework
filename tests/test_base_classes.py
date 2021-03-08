#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Test base classes

import pytest

from mframework._mframework import _BaseSpec, _UserSpaceBase
from mframework import log
log.on


def test_BaseSpec():

    class Spec(_BaseSpec):
        pass

    spec = Spec()
    spec._add_item_spec('a', int)
    spec._add_item_spec('b', int)

    assert repr(spec) == "<Specification for ('a', 'b')>"
    assert spec.keys == ['a', 'b']


def test_UserSpaceBase():

    class Spec(_BaseSpec):
        pass
    spec = Spec()
    spec._add_item_spec('a', int, max_items=1)
    spec._add_item_spec('b', float)

    class UserSpace(_UserSpaceBase):
        pass

    us = UserSpace()
    us._parent_specs = spec._specs

    us.set('a', 1)
    us.set('a', 42)  # Allow to override a singleton value

    with pytest.raises(TypeError):
        us.set('a', 42.5)

    us.add('b', 2.1)
    us.add('b', 2.2)
    us.add('b', 2.3)
    us.add_many('b', -1., -2., -3., -4.)

    with pytest.raises(TypeError):
        us.add_many('b', (-1., -2., -3., -4.))

    assert repr(us) == "<User space for ('a', 'b')>"

    # --- Singleton ---
    assert us.singleton('a') is True
    assert us.singleton('b') is False

    with pytest.raises(KeyError):
        us.singleton('KEY_DOES_NOT_EXIST')

    # --- get() ---
    assert us.get('a') == 42

    with pytest.raises(KeyError):
        us.get('KEY_DOES_NOT_EXIST')

    assert us.get('b') == [2.1, 2.2, 2.3, -1.0, -2.0, -3.0, -4.0]


