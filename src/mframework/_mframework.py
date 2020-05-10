#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2019-2020 Airinnova AB and the Model-Framework authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------

# Author: Aaron Dettmann

"""
Model framework
===============

    |    Model     <---   ModelSpec
    |      |                 |
    |      |                 |
    |   Feature   (<---) FeatureSpec
    |      |
    |      |
    |  (Property)
"""

from collections.abc import MutableMapping
from uuid import uuid4

from schemadict import schemadict

from ._log import logger

PRIMITIVE_TYPES = (bool, int, float, str, dict, list, tuple)


def is_primitve_type(obj):
    return obj in PRIMITIVE_TYPES


class DictLike(MutableMapping):
    """
    Dictionary-like object.

    * Keys must be strings.
    """

    def __init__(self, *args, **kwargs):

        self.mapping = {}
        self.update(*args, **kwargs)

    def __str__(self):
        return f"{self.mapping!r}"

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.mapping!r})"

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"invalid key {key!r}: must be of type {str}, not {type(key)}")

        self.mapping[key] = value

    def __getitem__(self, key):
        return self.mapping[key]

    def __delitem__(self, key):
        del self.mapping[key]

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)


class SpecDict(DictLike):
    """
    Specification dictionary.

    * Specification entries can only be defined once.
    """

    def __setitem__(self, key, value):
        if key in self.mapping.keys():
            raise KeyError(f"entry {key!r} already defined")
        super().__setitem__(key, value)


# TODO --> keep reference of parent spec in ItemDict
class ItemDict(DictLike):
    """
    Item dictionary.

    * Similar to a 'defaultdict(list)'
    """

    def __getitem__(self, key):
        if key not in self.mapping.keys():
            self.__missing__(key)
        return self.mapping[key]

    def __missing__(self, key):
        self.mapping[key] = list()


class SpecEntry:
    """
    Specification entry.
    """

    def __init__(self, schema, singleton=True, required=False, doc=''):
        self.schema = schema
        self.singleton = singleton
        self.required = required
        self.doc = doc

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, schema):
        self._schema = schema

    @property
    def singleton(self):
        return self._singleton

    @singleton.setter
    def singleton(self, singleton):
        self._check_type_bool('singleton', singleton)
        self._singleton = singleton

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, required):
        self._check_type_bool('required', required)
        self._required = required

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, doc):
        self._doc = doc

    @staticmethod
    def _check_type_bool(var_name, var):
        if not isinstance(var, bool):
            raise TypeError(f"invalid type for {var_name}: expected {bool}, got {type(var)}")


class _BaseSpec:
    """
    Base class to store a collection of item specifications.

    The term 'item' may refer to a property (e.g. the number 5) if this class
    describes a feature, or it may also refer to a feature itself if this class
    describes a model.
    """

    def __init__(self):
        """
        Attrs:
            :uid: (str) unique identifier
            :_specs: (dict) specifications (value) of items (key)
        """

        self.uid = str(uuid4())
        self._specs = SpecDict()

    def __repr__(self):
        return f"<Specification for {tuple(self._specs.keys())}>"

    def add_item_spec(self, key, schema, *, singleton=True, required=False, doc=''):
        """
        Add a specification

        Args:
            :key: (str) name of item to specify
            :schema: (obj) specification
            :singleton: (bool) if True, make item singleton
            :required: (bool) if True, make item required
            :doc: (str) documentation

        Note:
            * When calling from subclass, add a user input check for 'schema'
        """

        self._specs[key] = SpecEntry(schema, singleton, required, doc)

    def _provide_user_class_from_base(self, base):
        """
        Return a user space class which subclasses from 'base'

        Args:
            :base: (obj) base class

        Returns:
            :UserSpace: (obj) user space class with specification reference
        """

        class UserSpace(base):
            _parent_specs = self._specs
            _parent_uid = self.uid

        return UserSpace

    def get_docs(self):
        """
        Return user documentation

        Returns:
            :docs: (dict) full documentation
        """

        docs = {}
        for key, spec in self._specs.items():
            subdocs = None
            if isinstance(getattr(spec, 'schema', None), _BaseSpec):
                subdocs = spec.schema.get_docs()

            docs[key] = {
                'main': self._specs[key].doc,
                'schema': self._specs[key].schema,
                'sub': subdocs,
            }

        return docs


class _UserSpaceBase:
    """
    Base class for user space functionality for 'model' or 'feature'.
    """

    _parent_specs = None
    _parent_uid = None

    def __init__(self):
        """
        Attrs:
            :uid: (str) unique identifier
            :_specs: (dict) specifications (value) of items (key)
        """
        self.uid = str(uuid4())
        self._items = ItemDict()

    def from_dict(self, dictionary):
        """
        Add user values from a dictionary

        Args:
            :dictionary: (dict) key-value pairs
        """

        for key, value in dictionary.items():
            self._check_key_in_spec(key)
            if self._parent_specs[key].singleton:
                self.set(key, value)
            else:
                self.add(key, value)
        return self

    def to_dict(self):
        """
        TODO
        """

        return self._items

    def set(self, key, value):
        """
        TODO
        """

        self._check_key_in_spec(key)
        self._check_against_schema(key, value)

        if not self._parent_specs[key].singleton:
            raise RuntimeError(f"method 'set()' does not apply to {key!r}, try 'add()'")

        logger.debug(f"Set property {key!r} = {value!r}")
        self._items[key] = [value, ]

    def add(self, key, value):
        """
        TODO
        """

        self._check_key_in_spec(key)
        self._check_against_schema(key, value)

        if self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'add()' does not apply to {key!r}, try 'set()'")

        logger.debug(f"Add property {key!r} = {value!r} (num: {len(self._items[key])+1})")
        self._items[key].append(value)

    def add_many(self, key, values):
        """
        TODO
        """

        if not isinstance(values, (list, tuple)):
            raise TypeError("'values' must be list or tuple")

        for value in values:
            self.add(key, value)

    def get(self, key):
        """
        TODO
        """

        if self._parent_specs[key].singleton:
            return self._items[key][0]
        else:
            return self._items[key]

    def iter(self, key):

        if self._parent_specs[key].singleton:
            raise KeyError(f"Method 'iter()' not supported for item {key!r}, try 'get()'")

        yield from self._items[key]

    def len(self, key):
        return len(self._items[key])

    def _check_key_in_spec(self, key):
        if key not in self._parent_specs.keys():
            raise KeyError(f"key {key!r} is not in specification")

    def _check_against_schema(self, key, value):
        if isinstance(self._parent_specs[key].schema, dict):
            if not isinstance(value, dict):
                schemadict({'v': self._parent_specs[key].schema}).validate({'v': value})
            else:
                schemadict(self._parent_specs[key].schema).validate(value)
        elif not isinstance(value, self._parent_specs[key].schema):
            raise ValueError(f"invalid type for {key!r}: expected {self._parent_specs[key].schema}, got {type(value)}")


class FeatureSpec(_BaseSpec):

    def add_prop_spec(self, key, schema, *, singleton=True, required=False, doc=''):
        """
        TODO
        """

        if not (is_primitve_type(schema) or isinstance(schema, dict)):
            raise TypeError(f"'schema' must be a primitive type or a schemadict")

        if is_primitve_type(schema):
            schema = {'type': schema}

        super().add_item_spec(
            key,
            schema,
            singleton=singleton,
            required=required,
            doc=doc,
        )

    def provide_user_class(self):
        """
        TODO
        """

        return super()._provide_user_class_from_base(_UserSpaceBase)


class ModelSpec(_BaseSpec):

    def add_feature_spec(self, key, feature_spec, *, singleton=True, required=True, doc=''):

        if not isinstance(feature_spec, FeatureSpec):
            raise TypeError(f"'feature_spec' must be instance of 'FeatureSpec'")

        super().add_item_spec(
            key,
            feature_spec,
            singleton=singleton,
            required=required,
            doc=doc
        )

    def provide_user_class(self):
        """
        Return a 'Model' class with user and user methods
        """

        return super()._provide_user_class_from_base(_ModelUserSpace)


class _ModelUserSpace(_UserSpaceBase):

    def from_dict(self, dictionary):
        for key, feature_dict in dictionary.items():
            # TODO: check key in specification
            if self._parent_specs[key].singleton:
                feature = self.set_feature(key)
            else:
                feature = self.add_feature(key)
            feature.from_dict(feature_dict)
        return self

    def set(self, key, _):
        return NotImplementedError

    def add(self, key, _):
        return NotImplementedError

    def set_feature(self, key):
        """
        Make a singleton feature

        Args:
            :key: (str) name of the feature

        Returns:
            :feature: (obj) feature instance
        """

        # TODO: check: 'key' is string
        # TODO: check: feature exists in specification...

        if not self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'set_feature()' does not apply to {key!r}, try 'add_feature()'")

        logger.debug(f"Set feature {key!r}")
        f_instance = self._parent_specs[key].schema.provide_user_class()()
        self._items[key] = [f_instance, ]  # Store instance as list of length 1
        return f_instance

    def add_feature(self, key):
        """
        Add a non-singleton feature

        Args:
            :key: (str) name of the feature

        Returns:
            :feature: (obj) feature instance
        """

        # TODO: check: 'key' is string
        # TODO: check: feature exists in specification...

        if self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'add_feature()' does not apply to {key!r}, try 'set_feature()'")

        logger.debug(f"Add feature {key!r} (num: {len(self._items[key]) + 1})")
        f_instance = self._parent_specs[key].schema.provide_user_class()()
        self._items[key].append(f_instance)
        return f_instance
