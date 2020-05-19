What is |name|?
===============

|Name| is a framework to build simple to use Python interfaces for complex models. For instance, a structural analysis tool (like `FramAT <https://github.com/airinnova/framat>`_) requires a number of user inputs parameters, for instance, for general settings, material or loads. It can be cumbersome to develop a consistent user interface for such a tool which has a large number of settings. |Name| helps to build good Python user API's for complex models. In particular it aims to improve the following aspects of the developer and user experience.

* Providing a simple to understand Python API to build and interact with complex models
* Enforcing API consistency
* User input validation
* Full API documentation through automatic documentation generation
* Flexible model extensibility
* Clear separation between user input and solution routines

Developer and user
------------------

In this documentation we will use the terms *developer* and *user*. Here, we understand the *developer* to be the creator of a (physical) model (such as a structural analysis tool). The *user* (or *end user*) is the person who actually performs concrete computations (like for example computing the deflection of a structural beam).

For the developer, |name| provides two classes, namely ``FeatureSpec`` and ``ModelSpec`` to specify and build the user interface for a model. Conceptually, a model is made up of *features*, and each feature is made up of *properties*. The developer defines the model using specifications of model features and feature properties (user input).

The end user of the final model object can only interact with safe "setter" and "getter" methods of the specified model object. Due to the small number of simple methods which follow a clear "key-value paradigm" the model API is easy to learn and to document. As a model developer, you can easily enforce user-input checks to avoid invalid data. Expected input is defined in a simple schema format, and user-input checks are performed when data entered by the user.

Where to continue
-----------------

If you want to learn more about |name|, please check out the :ref:`sec_tutorial`.
