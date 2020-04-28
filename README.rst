===============================
qarrayrun
===============================


.. Image showing the PyPI version badge - links to PyPI
.. image:: https://img.shields.io/pypi/v/qarrayrun.svg
        :target: https://pypi.python.org/pypi/qarrayrun

.. Image showing the Travis Continuous Integration test status, commented out for now
.. .. image:: https://img.shields.io/travis/CFSAN-Biostatistics/qarrayrun.svg
..        :target: https://travis-ci.org/CFSAN-Biostatistics/qarrayrun



A helper tool for running array jobs on an HPC computational node.

The qarrayrun package was developed by the United States Food
and Drug Administration, Center for Food Safety and Applied Nutrition.

This script executes a single slot of an array job on an HPC compute node.
It is intended to be used with Sun Grid Engine, SLURM, or Torque job schedulers.
It assumes every instance of the job array runs the same command but with
different arguments.  This script performs the work of looking-up the
arguments in a text file and substituting those arguments into the command
to be executed.

* Free software
* Documentation: https://qarrayrun.readthedocs.io
* Source Code: https://github.com/CFSAN-Biostatistics/qarrayrun
* PyPI Distribution: https://pypi.python.org/pypi/qarrayrun


Features
--------

* Executes a single slot of an array job on an HPC compute node
* Simple parameter lookup language
* Supports execution in a subshell when needed


Citing qarrayrun
--------------------------------------

To cite qarrayrun, please reference the qarrayrun GitHub repository:

    https://github.com/CFSAN-Biostatistics/qarrayrun


License
-------

See the LICENSE file included in the qarrayrun distribution.

