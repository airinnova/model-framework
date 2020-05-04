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

    |   Model     <---   ModelSpec
    |     |                 |
    |     |                 |
    |  Feature   (<---) FeatureSpec
    |     |
    |     |
    |  (Property)
"""

from collections import namedtuple, defaultdict
from uuid import uuid4

from schemadict import schemadict

from ._log import logger

PRIMITIVE_TYPES = (bool, int, float, str, dict, list, tuple)


def is_primitve_type(obj):
    return obj in PRIMITIVE_TYPES


class FeatureSpec:

    # Every feature has one or more properties.
    # Each property is defined by a property specification.
    _PROP_SPEC_ENTRY = namedtuple(
        'PropSpec',
        ['schema', 'singleton', 'required']
    )

    def __init__(self):
        """
        Class to build feature specifications

        Attr:
            :uid: (str) unique identifier
            :_prop_specs: (dict) specification of expected user data
        """

        self.uid = str(uuid4())
        self._prop_specs = {}

    def add_prop_spec(self, key, schema, *, singleton=True, required=False):
        """
        Add a specification for a feature property defined by a key-value pair

        Args:
            :key: (str) name of the property
            :schema: (any) schemadict or type of expected value
            :singleton: (bool) if True, make property singleton
            :required: (bool) if True, property must be defined
        """

        if not isinstance(key, str):
            raise TypeError(f"'key' must be of type string, got {type(key)}")

        if not (is_primitve_type(schema) or isinstance(schema, dict)):
            raise TypeError(f"'schema' must be a primitive type or a schemadict")

        for arg in (singleton, required):
            if not isinstance(arg, bool):
                raise TypeError(f"argument of type boolean expected, got {type(arg)}")

        # Keys must be unique, do not allow to overwrite
        if key in self._prop_specs.keys():
            raise KeyError(f"Property {key!r} already defined")

        self._prop_specs[key] = self._PROP_SPEC_ENTRY(schema, singleton, required)

    def provide_user_class(self):
        """
        Return a 'Feature' class with user storage and user methods
        """

        class Feature(_FeatureUserSpace):
            # Class variables
            _parent_specs = self._prop_specs  # Reference to property specifications
            _parent_uid = self.uid

        return Feature


class _FeatureUserSpace:

    _parent_specs = None
    _parent_uid = None

    def __init__(self):
        """
        This class provides user storage and user methods

        This class should only be derived from 'FeatureSpec'

        Attr:
            :uid: (str) unique identifier
            :_props: (dict) storage of user data
        """

        self.uid = str(uuid4())
        self._props = defaultdict(list)

    def __repr__(self):
        return f"<Feature {self.uid!r} (parent: {self._parent_uid!r})>"

    def set(self, key, value):
        """
        Set a value (singleton property)

        Args:
            :key: (str) name of the property
            :value: (any) value of the property
        """

        self._raise_err_key_not_allowed(key)
        self._raise_err_incorrect_type(key, value)

        if not self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'set()' does not apply to {key!r}, try 'add()'")

        logger.debug(f"Set property {key!r} = {value!r}")
        self._props[key] = [value, ]  # Store as list of length 1

    def add(self, key, value):
        """
        Add a value (non-singleton property)

        Args:
            :key: (str) name of the property
            :value: (any) value of the property
        """

        self._raise_err_key_not_allowed(key)
        self._raise_err_incorrect_type(key, value)

        if self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'add()' does not apply to {key!r}, try 'set()'")

        logger.debug(f"Add property {key!r} = {value!r} (num: {len(self._props[key])+1})")
        self._props[key].append(value)

    def add_many(self, key, values):
        # TODO: check: values --> list or tuple
        for value in values:
            self.add(key, value)

    def get(self, key):
        """
        Return the stored properties

        Args:
            :key: (str) name of the property
        """

        # TODO: check key is valid (i.e. in specification)...
        # TODO: check that list not empty...

        if self._parent_specs[key].singleton:
            return self._props[key][0]
        else:
            return self._props[key]

    def iter(self, key):
        """
        Return a generator to iterate over set of properties

        Args:
            :key: (str) name of the property
        """

        if self._parent_specs[key].singleton:
            raise KeyError(f"Method 'iter()' not supported for property {key!r}, try 'get()'")

        yield from self._props[key]

    def len(self, key):
        """
        Return the number of items for property 'key'
        """

        # TODO: check if key in specification (i.e. in '_parent_specs')...
        # TODO: check if key in dict (i.e. in '_props')...

        return len(self._props[key])

    # TODO: move check functions!?

    def _raise_err_key_not_allowed(self, key):
        if key not in self._parent_specs.keys():
            raise KeyError(f"Key {key!r} is not in specification")

    def _raise_err_incorrect_type(self, key, value):
        if isinstance(self._parent_specs[key].schema, dict):
            if not isinstance(value, dict):
                schemadict({'v': self._parent_specs[key].schema}).validate({'v': value})
            else:
                schemadict(self._parent_specs[key].schema).validate(value)
        elif not isinstance(value, self._parent_specs[key].schema):
            raise ValueError(f"Value of type {self._parent_specs[key].schema} expected, got {type(value)}")


class ModelSpec:

    _FEATURE_SPEC_ENTRY = namedtuple(
        'FeatureSpec',
        ['spec', 'singleton']
    )

    def __init__(self):
        """
        Class to build model specifications

        Attr:
            :uid: (str) unique identifier
            :_feature_specs: (dict) specification of expected user data
        """

        self.uid = str(uuid4())
        self._feature_specs = {}

    def add_feature_spec(self, key, feature_spec, *, singleton=True):
        """
        Add a specification for a model feature

        Args:
            :key: (str) name of the feature
            :feature_spec: instance of 'FeatureSpec'
            :singleton: (bool) if True, make feature singleton
        """

        if not isinstance(key, str):
            raise TypeError(f"'key' must be of type string, got {type(key)}")

        if not isinstance(feature_spec, FeatureSpec):
            raise TypeError(f"'feature_spec' must be instance of 'FeatureSpec'")

        if not isinstance(singleton, bool):
            raise TypeError(f"Argument 'singleton' must be of type bool")

        # Keys must be unique, do not allow overwrite
        if key in self._feature_specs.keys():
            raise KeyError(f"Feature {key!r} already defined")

        self._feature_specs[key] = self._FEATURE_SPEC_ENTRY(feature_spec, singleton)

    def provide_user_class(self):
        """
        Return a 'Model' class with user and user methods
        """

        class Model(_ModelUserSpace):
            # Class variables
            _parent_specs = self._feature_specs  # Reference to specifications
            _parent_uid = self.uid

        return Model


class _ModelUserSpace:

    _parent_specs = None
    _parent_uid = None

    def __init__(self):
        """
        This class provides user storage and user methods

        This class should only be derived from 'ModelSpec'

        Attr:
            :uid: (str) unique identifier
            :_features: (dict) storage of user data
        """

        self.uid = str(uuid4())
        self._features = defaultdict(list)

    def __repr__(self):
        return f"<Model {self.uid!r}>"

    def set_feature(self, key):
        """
        Make a singleton feature

        Args:
            :key: (str) name of the feature

        Returns:
            :feature: (obj) feature instance
        """

        # TODO:
        # * Check that feature exists in specification...

        if not self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'set_feature()' does not apply to {key!r}, try 'add_feature()'")

        logger.debug(f"Set feature {key!r}")
        f_instance = self._parent_specs[key].spec.provide_user_class()()
        self._features[key] = [f_instance, ]  # Store instance as list of length 1
        return f_instance

    def add_feature(self, key):
        """
        Add a non-singleton feature

        Args:
            :key: (str) name of the feature

        Returns:
            :feature: (obj) feature instance
        """

        # TODO:
        # * Check that feature exists in specification...

        if self._parent_specs[key].singleton:
            raise RuntimeError(f"Method 'add_feature()' does not apply to {key!r}, try 'set_feature()'")

        logger.debug(f"Add feature {key!r} (num: {len(self._features[key]) + 1})")
        f_instance = self._parent_specs[key].spec.provide_user_class()()
        self._features[key].append(f_instance)
        return f_instance

    def get(self, key):
        # TODO: ...
        if self._parent_specs[key].singleton:
            return self._features[key][0]
        else:
            return self._features[key]

    def iter(self, key):
        # TODO: ...
        if self._parent_specs[key].singleton:
            raise KeyError(f"Method 'iter()' not supported for feature {key!r}, try 'get()'")
        yield from self._features[key]
