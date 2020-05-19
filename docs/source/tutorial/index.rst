.. _sec_tutorial:

Tutorial
========

This example will walk you through the basic process of building a model with the |name|, and also demonstrate how to provide a simple, and documented user interface.

What we want to achieve?
------------------------

Let's start at the end. What do we actually want to achieve here? We want to build a simple Python user interface for a model. As an example, let's consider a very simple aircraft model. We will implement the so-called `Breguet range equation <https://en.wikipedia.org/wiki/Range_(aeronautics)>`_ which can be used to estimate the range of an aircraft. According to the Breguet equtation, the range for a jet aircraft in cruise conditions can be estimated from the following relation.

.. math::

    R = \frac{a \, M}{g \, c_\textrm{T}} \, \frac{C_\textrm{L}}{C_\textrm{D}} \, \textrm{ln} \, \frac{m_1}{m_2}

* :math:`R`: range
* :math:`a`: speed of sound
* :math:`M`: Mach number
* :math:`c_\textrm{t}`: thrust specific fuel consumption
* :math:`C_\textrm{L}`: lift coefficient
* :math:`C_\textrm{D}`: drag coefficient
* :math:`m_1`: initial mass
* :math:`m_2`: final mass

The exact meaning, derivation and limitation of this formula are not relevant for the following discussion. What we want, is to provide a Python API which picks up and validates the user input. The user API can be used in the following way:

.. code:: python

    >>> from aircraft import Model

    >>> # First, we create a new aircraft model instance
    >>> ac = Model()

    >>> # In our case the aircraft model, will have the feature 'aerodynamics'.
    >>> # Below, we first create an instance of this feature, and subsequently
    >>> # we assign numerical values to the aerodynamic properties.
    >>> aero = ac.set_feature('aerodynamics')
    >>> aero.set('CL', 1.5)
    >>> aero.set('CD', 0.005)
    >>> aero.set('Mach', 0.8)

    >>> # Our aircraft model also has a 'propulsion' feature.
    >>> # In this feature we set the specific fuel consumption.
    >>> prop = ac.set_feature('propulsion')
    >>> prop.set('cT', 1.5)

    >>> # Finally, we have a third feature called 'mass' which we will make
    >>> # 'non-singleton' for demonstration purposes. So let's assign values
    >>> # to masses 'm1' and 'm2'
    >>> mass_conf1 = ac.add_feature('mass')
    >>> mass_conf1.set('m1', 1)
    >>> mass_conf1.set('m2', 2)

    >>> # We may also add a second mass configuration, for example:
    >>> mass_conf2 = ac.add_feature('mass')
    >>> mass_conf2.set('m1', 2)
    >>> mass_conf2.set('m2', 3)

    >>> # Once, we have set up the model we can call the 'run()' method which
    >>> # will compute the range for both configurations and print the results.
    >>> ac.run()
    The range for xx and yy is: xxx km
    The range for xx and yy is: xxx km
    >>>

Of course, the model discussed here is very simple, and it would not make sense to provide such an elaborate and explicit API to solve the simple range formula. However, for complex models it may become much harder to provide a user interface which is simple to use and extensible, and it may become hard to document all available user inputs. The |name| addresses these issues.

How do we build the API?
------------------------

Python module file structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will assume the following file structure for our example:

.. code::

    aircraft/
        __init__.py
        _model.py
        _run.py

Our goal is to provide the ``Model`` object that we used above and that provide all user methods. Why we organize our module Python files in the structure as suggested above, will hopefully become clearer as we go along in this tutorial.

Building the user class
-----------------------

Let's start at the end: we want the user to import our model with ``from aircraft import Model``. To achive this, we provide a reference to the ``Model`` object in the ``__init__.py``.

.. literalinclude:: aircraft/__init__.py
    :language: python

Okay, but so far the file ``_model.py`` is empty, and does not contain the object ``Model``. The code below shows how.

.. literalinclude:: aircraft/_model.py
    :language: python
    :lines: 4-

Finally, ...

.. literalinclude:: aircraft/_run.py
    :language: python
    :lines: 5-

Using the user class
~~~~~~~~~~~~~~~~~~~~

**TODO**

How do we build user documentation?
-----------------------------------

**TODO**

.. toctree::
   :maxdepth: 1
   :caption: Auto-generated documentation

   autodoc/model_api_general
   autodoc/model_api
   autodoc/result_api

Further options and references
------------------------------

* ...
* Link to schemadict documentation/repo
