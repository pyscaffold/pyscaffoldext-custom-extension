.. image:: https://api.cirrus-ci.com/github/pyscaffold/pyscaffoldext-custom-extension.svg?branch=master
    :alt: Travis
    :target: https://cirrus-ci.com/github/pyscaffold/pyscaffoldext-custom-extension
.. image:: https://readthedocs.org/projects/pyscaffoldext-custom-extension/badge/?version=latest
    :alt: ReadTheDocs
    :target: https://pyscaffoldext-custom-extension.readthedocs.io/
.. image:: https://img.shields.io/coveralls/github/pyscaffold/pyscaffoldext-custom-extension/master.svg
    :alt: Coveralls
    :target: https://coveralls.io/r/pyscaffold/pyscaffoldext-custom-extension
.. image:: https://img.shields.io/pypi/v/pyscaffoldext-custom-extension.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/pyscaffoldext-custom-extension/

|

==============================
pyscaffoldext-custom-extension
==============================

PyScaffold extension that let's you create your own custom extensions.


Description
===========

This extension serves as a support for the users interested in developing their own extension for PyScaffold. It configures your project so that you can start writing your extension logic and tests right away, taking care of all the wiring required to conform to PyScaffold's needs.

Let's say you want to create an extension named ``notebooks`` that creates a notebooks folder with some template `Jupyter notebook`_. After having installed this extension with::

 pip install pyscaffoldext-custom-extension

you will be able to just use it with::

 putup --custom-extension notebooks

This will create a typical PyScaffold project template with some modifications:

* the topmost namespace will be ``pyscaffoldext`` to have a unified namespace for PyScaffold extensions,
* assures that the package (as PyPI sees it) is named ``pyscaffoldext-notebooks`` in ``setup.cfg``,
* sets the correct ``install_requires`` as well as the ``options.entry_points`` parameters in ``setup.cfg``,
* automatically activates the extensions ``--no-skeleton``, ``--pre-commit``, ``--travis`` and
  since we want clean-coded, high-quality extensions,
* creates a ``extension.py`` module holding a class ``Notebooks`` which serves you as a template for your extension,
* adds basic unit tests checking that the invocation of your extension works and that it complies with our `flake8`_ code guidelines,
* provides a modified ``README.rst`` indicating that this is a PyScaffold extensions and how to install it.


.. pyscaffold-notes::

Making Changes & Contributing
=============================

This project uses `pre-commit`_, please make sure to install it before making any
changes::

    $ pip install pre-commit
    $ cd pyscaffoldext-custom-extension
    $ pre-commit install

It is a good idea to update the hooks to the latest version::

    pre-commit autoupdate

Please also check PyScaffold's own [CONTRIBUTING.rst file](https://github.com/pyscaffold/pyscaffold/blob/master/CONTRIBUTING.rst).


Note
====

For more information about PyScaffold and its extension mechanism, check out http://pyscaffold.org/.

.. _Jupyter notebook: https://jupyter-notebook.readthedocs.io/
.. _flake8: http://flake8.pycqa.org/
.. _pre-commit: http://pre-commit.com/
