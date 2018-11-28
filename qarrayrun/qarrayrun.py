# -*- coding: utf-8 -*-

"""This module is part of qarrayrun.
"""

from __future__ import print_function
from __future__ import absolute_import

import logging
import os
import re
import shlex
import subprocess


def get_file_line(file_name, line_num):
    """Returns the line at the specified line number from the specified file.

    Parameters
    ----------
    file_name : str
        Path to the file
    line_num : int
        Line number to extract from the file

    Returns
    -------
    line : str
        Line at line_num in file or None if the line_num is larger than the number of lines in the file
    """
    line = ""
    line_counter = 0
    with open(file_name) as f:
        for line in f:
            line_counter += 1
            if line_counter == line_num:
                return line
    return None


def substitute_arguments(command_line, arguments):
    """Replace the parameter placeholders in a command line with actual arguments.

    Parameters
    ----------
    command_line : str
        Command line with parameter placeholders like {1}, {2}, {3}
    arguments : list of str
        List of arguments numbered 1,2,3 ....
        The first argument, arguments[0] corresponds to placeholder {1}.

    Returns
    -------
    command_line : str
        Command line with actual arguments ready for execution

    Examples
    --------
    >>> substitute_arguments("cmd {0}/{1}/{2} -- {3}{4}", ["aa", "bb", "cc"])
    'cmd /aa/bb -- cc'
    """
    args = [""]  # put an empty string at index 0
    args.extend(arguments)

    # Get a list of all the parameter numbers appearing in the command line
    param_nums = re.findall("{([0-9]+)}", command_line)
    param_nums = [int(param_num) for param_num in param_nums]

    # Replace the parameters with actual arguments
    for param_num in param_nums:
        placeholder = "{%s}" % param_num
        if param_num == 0 or param_num >= len(args):
            command_line = command_line.replace(placeholder, "")
        else:
            command_line = command_line.replace(placeholder, args[param_num])

    return command_line


def run(subtask_var, array_file, command_line, shell_flag=False):
    """Execute a single subtask of an array job.

    Lookup the parameters for this subtask, substitute those parameters
    into the command line, and run the command.

    Parameters
    ----------
    subtask_var : str
        Name of the environment variable containing the subtask number.  This
        variable is created automatically by the HPC job execution software
        (Grid Engine or Torque).
    array_file : str
        Path to the file containing array job parameters with one line per array-job
        subtask.  This file must exist on a file system that is accessible to the
        compute nodes.
    command_line : str
        Command line with parameter placeholders like {1}, {2}, {3}
    shell_flag : bool, optional
        Boolean flag indicates if the command should be run in a subshell. Defaults to false.

    Returns
    -------
    int
        Return code of the command after it finishes execution
    """
    # Which sub-task number am I?
    subtask_num = os.environ.get(subtask_var)
    if not subtask_num:
        logging.error("Error: the %s environment variable is not defined." % subtask_var)
        exit(1)

    try:
        subtask_num = int(subtask_num)
    except ValueError:
        logging.error("Error: the %s environment variable does not contain a line number." % subtask_var)
        exit(1)

    if subtask_num <= 0:
        logging.error("Error: the subtask number is %d.  It must be greater than zero." % subtask_num)

    # Verify file exists
    if not os.path.isfile(array_file):
        logging.error("Error: the parameter file %s does not exist." % array_file)
        exit(1)

    # Read and parse the substitution arguments from the input file
    line = get_file_line(array_file, subtask_num)
    if not line:
        exit(0)  # Silently ignore attempts to process beyond the end of the file
    arguments = line.split()

    # Build the command with substituted arguments
    command_line = substitute_arguments(command_line, arguments)

    # Execute the command
    if shell_flag:
        return_code = subprocess.call(command_line, shell=True)
    else:
        command_split = shlex.split(command_line)
        return_code = subprocess.call(command_split, shell=False)
    return return_code
