What is |name|?
===============

Developer and user
------------------

In this documentation we will use the terms *developer* and *user*. Here, we understand the *developer* to be the creator of a (physical) model (such as a structural analysis tool). The *user* (or *end user*) is the person who actually performs concrete computations (like for example computing the deflection of a structural beam).

For the developer, |name| provides two classes, namely ``FeatureSpec`` and ``ModelSpec`` to specify and build the user interface for a model. Conceptually, a model is made up of *features*, and each feature is made up of *properties*. The developer defines the model using specifications of model features and feature properties (user input).

The end user of the final model object can only interact with safe "setter" and "getter" methods of the specified model object. Due to the small number of simple methods which follow a clear "key-value paradigm" the model API is easy to learn and to document. As a model developer, you can easily enforce user-input checks to avoid invalid data. Expected input is defined in a simple schema format, and user-input checks are performed when data entered by the user.

Where to continue
-----------------

If you want to learn more about |name|, please check out the :ref:`sec_tutorial`.
