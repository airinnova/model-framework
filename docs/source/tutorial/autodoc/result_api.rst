Results
=======

The method ``run()`` returns a ``Result`` object.
You can interact  with this object in the same way as the ``Model`` object
itself. The following results are available in the result object.



.. mermaid::

    graph TD
    A[Model]
    A --> F0[flight_mission]


Feature: flight_mission
-----------------------

.. image:: https://raw.githubusercontent.com/airinnova/model-framework/master/src/mframework/ressources/icons/point.svg
   :align: left
   :alt: singleton

*Singleton*: True

.. image:: https://raw.githubusercontent.com/airinnova/model-framework/master/src/mframework/ressources/icons/lifebuoy.svg
   :align: left
   :alt: required

*Required*: True

Property: range
~~~~~~~~~~~~~~~

.. mermaid::

    graph LR
    A[Model]
    A --> F1[flight_mission] 
    F1 --> P1[range] 


.. image:: https://raw.githubusercontent.com/airinnova/model-framework/master/src/mframework/ressources/icons/point.svg
   :align: left
   :alt: singleton

*Singleton*: True

.. image:: https://raw.githubusercontent.com/airinnova/model-framework/master/src/mframework/ressources/icons/lifebuoy.svg
   :align: left
   :alt: required

*Required*: True

.. image:: https://raw.githubusercontent.com/airinnova/model-framework/master/src/mframework/ressources/icons/clipboard-check.svg
   :align: left
   :alt: schema

*Schema*:

======== ===============
**type** <class 'float'>
 **>**          0       
======== ===============

