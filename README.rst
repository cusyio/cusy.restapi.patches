.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/cusyio/cusy.restapi.patches/workflows/ci/badge.svg
    :target: https://github.com/cusyio/cusy.restapi.patches/actions

.. image:: https://coveralls.io/repos/github/cusyio/cusy.restapi.patches/badge.svg?branch=master
    :target: https://coveralls.io/github/cusyio/cusy.restapi.patches?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/cusy.restapi.patches.svg
    :target: https://pypi.python.org/pypi/cusy.restapi.patches/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/cusy.restapi.patches.svg
    :target: https://pypi.python.org/pypi/cusy.restapi.patches
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/cusy.restapi.patches.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/cusy.restapi.patches.svg
    :target: https://pypi.python.org/pypi/cusy.restapi.patches/
    :alt: License


====================
cusy.restapi.patches
====================

Patches and fixes for plone.restapi which are not yet released.

Patches
-------

- Navigation endpoint should sort by object position in parent
  https://github.com/plone/plone.restapi/issues/1107


Installation
------------

Install ``cusy.restapi.patches`` by adding it to your buildout::

    [buildout]

    ...

    eggs =
        cusy.restapi.patches


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/cusyio/cusy.restapi.patches/issues
- Source Code: https://github.com/cusyio/cusy.restapi.patches


Support
-------

If you are having issues, please let us know by adding a new ticket.


License
-------

The project is licensed under the GPLv2.
