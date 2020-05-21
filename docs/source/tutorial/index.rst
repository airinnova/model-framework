.. _sec_tutorial:

How do I use it?
================

This example will walk you through the basic process of building a model with the |name|, and also demonstrate how to provide a simple, and documented user interface.

What we want to achieve?
------------------------

Let's start at the end. What do we actually want to achieve here? We want to build a simple Python user interface for a model. As an example, let's consider a very simple aircraft model. We will implement the so-called `Breguet range equation <https://en.wikipedia.org/wiki/Range_(aeronautics)>`_ which can be used to estimate the range of an aircraft. According to the Breguet equitation, the range for a jet aircraft in cruise conditions can be estimated from the following relation.

.. math::

    R = \frac{a \, M}{g \, c_\textrm{T}} \, \frac{C_\textrm{L}}{C_\textrm{D}} \, \textrm{ln} \, \frac{m_1}{m_2}

* :math:`R`: range [m]
* :math:`a`: speed of sound [m/s]
* :math:`M`: Mach number [1]
* :math:`c_\textrm{T}`: thrust specific fuel consumption [kg/(s*N)]
* :math:`C_\textrm{L}`: lift coefficient [1]
* :math:`C_\textrm{D}`: drag coefficient [1]
* :math:`m_1`: initial mass [kg]
* :math:`m_2`: final mass [kg]

The exact derivation and limitation of this formula are not relevant for the following discussion. What we want, is to provide a Python API which picks up and validates the user input. The user API can be used in the following way:

.. literalinclude:: example.py
    :lines: 4-
    :language: python

When running this example, we get rages for the chosen combinations of initial and final masses.

..
    # Add to PYTHONPATH, to run doctest on the following example
    >>> import sys
    >>> sys.path.append("docs/source/tutorial/")
    >>>

.. code::

    >>> import example
    Range: 15914.1 km (m1: 70.0 t | m2: 35.0 t)
    Range: 12848.3 km (m1: 70.0 t | m2: 40.0 t)
    Range: 10144.1 km (m1: 70.0 t | m2: 45.0 t)
    Range:  7725.1 km (m1: 70.0 t | m2: 50.0 t)
    Range:  5536.9 km (m1: 70.0 t | m2: 55.0 t)
    Range:  3539.2 km (m1: 70.0 t | m2: 60.0 t)
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

Our goal is to provide the ``Model`` object that we used above and that provides all user methods. Why we organize our module Python files in the structure as suggested above, will hopefully become clearer as we go along in this tutorial.

Building the user class
-----------------------

Let's start at the end: we want the user to import our model with ``from aircraft import Model``. To achive this, we provide a reference to the ``Model`` object in the ``__init__.py``.

.. literalinclude:: aircraft/__init__.py
    :language: python

Okay, but so far the file ``_model.py`` is empty, and does not contain the object ``Model``. The code below shows how.

.. literalinclude:: aircraft/_model.py
    :language: python
    :lines: 4-

When defining the method ``run()`` in ``Model``, we passed the model instance to another method called ``run_model``. We define this method in the file ``_run.py``.

.. literalinclude:: aircraft/_run.py
    :language: python
    :lines: 4-

That's it. In this simplistic example, the procedure may rightfully seem very elaborate and perhaps overly complicate. However, for complex models this process pay off, not at least for the user documentation which can be generated fully automatically.

How do we build user documentation?
-----------------------------------

Below, you will see the actual script which is used to generate the documentation in this tutorial.

.. literalinclude:: docgen.py
    :language: python
    :lines: 4-

After running this script, we get the following pages:

.. toctree::
   :maxdepth: 1

   autodoc/model_api_general
   autodoc/model_api
   autodoc/result_api

Further options and references
------------------------------

:API documentation:
    For a more comprehensive overview about the functionality, please check out the API documentation for |name|.

:schemadict:
    More details about *schemadict* can be found here: https://github.com/airinnova/schemadict.
