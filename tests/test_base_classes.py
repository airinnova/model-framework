#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    us.add('b', 2.1)
    us.add('b', 2.2)

    assert repr(us) == "<User space for ('a', 'b')>"
