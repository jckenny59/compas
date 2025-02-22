****************
Working in Rhino
****************

.. rst-class:: lead

The core library of COMPAS (:mod:`compas`), and the Rhino CAD package (:mod:`compas_rhino`)
are backwards compatible with Python 2.7 and written in pure Python,
such that they can be used in Rhino IronPython scripts (Rhino 7 and below),
as well as in the new Rhino CPython scripts (Rhino 8).

.. warning::

    These instructions are for Rhino 6 and 7.
    For Rhino 8, please refer to :doc:`/userguide/cad.rhino8`.

Installation
============

To use COMPAS in Rhino 6 or 7, you need to make Rhino aware of your COMPAS installation.
This can be done with a simple command on the command line.

.. note::

    Assuming COMPAS is installed in a ``conda`` environment, make sure to activate the environment before running any of the commands below.
    It is recommended to also close Rhino before running the commands.
    If Rhino was still running, it will have to restarted before the changes take effect.

.. code-block:: bash

    python -m compas_rhino.install

This will install all Rhino-compatible packages of COMPAS that are present in the current Python environment into Rhino.
It will also automatically install all GH Components that are available for the installed packages.
Once the command terminates, you should see a message like this:

.. code-block:: bash

    ...


The default Rhino version is 7.
To install into Rhino 6, use the ``-v`` flag.

.. code-block:: bash

    python -m compas_rhino.install -v 6.0

Note that if COMPAS is installed in a ``conda`` environment, you need to activate it the environment before running the command.

.. code-block:: bash

    conda activate compas-dev
    python -m compas_rhino.install


Sample Script
=============

To test if the installation was successful, you can run the following script in Rhino.

.. code-block:: python

    import compas
    import compas_rhino

    print(compas.__version__)


Visualisation
=============


Conversions
===========


Data Exchange
=============


Remote Procedure Calls
======================


Known Issues
============

