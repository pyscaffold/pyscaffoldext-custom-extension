=========
Changelog
=========

Version 0.6.3
=============

- Update dependencies to include ConfigUpdater 3.x

Version 0.6.2
=============

- Update configupdater to version >= 2.0

Version 0.6.1
=============

- Ensure generated extension is tested in combination with ``--namespace``, #24

Version 0.6
===========

- Changes required for PyScaffold v4.0
- Updated templates for testing
- Simplified templates package thanks to ``pyscaffold.templates.get_template``
- Removed unnecessary ``coding: utf-8`` comments
- Replaced ``travis`` with ``cirrus`` extension
- Version scheme changed to ``no-guess-dev`` (from ``setuptools_scm``)
- Fixed references to PyScaffold in the docs, by adding it as a doc requirement, #23
- Added Github Actions template for automatically publishing tags to PyPI

Version 0.5
===========

- Add ``pyscaffoldext`` by default warning the user

Version 0.4.1
=============

- Cosmetic changes

Version 0.4
===========

- Always set namespace to ``pyscaffoldext``
- Changes required for PyScaffold 3.2
- Several fixes

Version 0.3
===========

- Docstrings in Google Format
- Added conftest.py as template
- Reworked README.rst template
- Added default unit test for extension
- Few fixes

Version 0.2
===========

- Check for pyscaffoldext naming convention
- Added new README.rst
- Check with flake8
- Added testing requirements
- Usage of tox

Version 0.1
===========

- First release
