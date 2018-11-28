# -*- coding: utf-8 -*-

"""
test_qarrayrun
----------------------------------

Tests for `qarrayrun` module.
"""

from __future__ import print_function

import os

from qarrayrun import qarrayrun


def test_run():
    # Create array job parameter file
    from tempfile import NamedTemporaryFile
    f = NamedTemporaryFile(delete=False, mode='w')
    arg_file = f.name
    print("A B C", file=f)
    print("Argument1 Argument2 Argument3", file=f)
    f.close()
    f = NamedTemporaryFile(delete=False, mode='w')
    out_file = f.name

    # Write the arguments in reverse order to out_file
    cmd = "python -c '"
    cmd += 'f = open("%s", "w");' % out_file
    cmd += 'f.write("{3} {2} {1}"); f.close()'
    cmd += "'"
    os.environ["SGE_TASK_ID"] = "2"
    return_code = qarrayrun.run("SGE_TASK_ID", arg_file, cmd)
    assert(return_code == 0)

    # Read the file just created to verify reverse order
    f = open(out_file)
    s = f.read()
    f.close()
    assert(s == "Argument3 Argument2 Argument1")

    # Verify non-zero exit code can be returned
    return_code = qarrayrun.run("SGE_TASK_ID", arg_file, "exit 100", shell_flag=True)
    assert(return_code == 100)

    # Clean up temp files
    os.unlink(arg_file)
    os.unlink(out_file)
