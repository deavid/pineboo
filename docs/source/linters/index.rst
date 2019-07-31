Static Analysis on Pineboo code
===================================

On our efforts for best code quality we also run several tools performing
static analysis on Pineboo sources. Sadly, we're still far from havign those
tools pass without error, so they cannot be implemented on our CI/CD pipeline.

Instead, we gather their reports into this page.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   pylint/pylint
   mypy/index
   pytest-coverage/index
