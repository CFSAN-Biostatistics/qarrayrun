#!/usr/bin/env python

"""Console script for qarrayrun.

This script executes a single slot of an array job on an HPC compute node.
It is intended to be used with Sun Grid Engine or Torque job schedulers.
It assumes every instance of the job array runs the same command but with
different arguments.  This script performs the work of looking-up the
arguments in a text file and substituting those arguments into the command
to be executed.

Parameters
----------
The script takes 3 arguments:

1. Name of the environment variable that contains the sub-task number.
   You should use SGE_TASK_ID for grid engine.
   You should use PBS_ARRAYID for torque.

2. Name of the file containing the arguments for each sub-task with one line
   per sub-task.  This script will extract the arguments for this sub-task
   at the line number identified by the environment variable above.  The
   line is parsed and substituted into the command, replacing the parameter placeholders
   with the actual arguments.

3. The remainder of the command line is the command to be executed with parameter
   placeholders of the form {1}, {2}, {3} ...

Examples
--------
# Sort some txt files, writing the sorted output to new files
ls *.txt > files.txt
echo 'qarrayrun.py SGE_TASK_ID files.txt sort -o sorted.{1} {1}' | qsub -t 1-$(cat files.txt | wc -l) -cwd -j y -V -o log

# Your input file might have multiple columns, use {2} for the 2nd column
# Sort the largest files first
ls *.txt | xargs -n 1 wc -c | sort -n -r > files.txt
echo 'qarrayrun.py SGE_TASK_ID files.txt sort -o sorted.{2} {2}' | qsub -t 1-$(cat files.txt | wc -l) -cwd -j y -V -o log

# Use the --shell option and quote your pipeline when you need shell redirection
# Remove blanks before sorting files
ls *.txt > files.txt
echo 'qarrayrun --shell SGE_TASK_ID files.txt "cat {1} | tr -d [:blank:] | sort > sorted.{1}"' | qsub -t 1-$(cat files.txt | wc -l) -cwd -j y -V -o log
"""

from __future__ import print_function
from __future__ import absolute_import

import argparse
import logging
import sys
import textwrap

from qarrayrun import qarrayrun
from qarrayrun.__init__ import __version__

# Ignore flake8 errors in this module
# flake 8: noqa


def parse_arguments(system_args):
    """Parse command line arguments.

    This is an unusual command line parser -- it only parses the command-line
    arguments it expects, and captures the remaining arguments to pass along
    to the function processing the command.

    Parameters
    ----------
    system_args : list
        List of command line arguments, usually sys.argv[1:].

    Returns
    -------
    Namespace
        Command line arguments are stored as attributes of a Namespace.
    list
        List of remaining argument strings
    """
    description = textwrap.dedent("""
        Executes a single slot of an array job on an HPC computational node. This is
        intended to be used with Sun Grid Engine or Torque job schedulers when every
        instance of the job array runs the same command but with different arguments.
        This script performs the work of looking-up the arguments in a text file and
        substituting those arguments into the command to be executed.""")

    epilog = textwrap.dedent("""
        Examples
        --------
        # Sort some txt files, writing the sorted output to new files
        ls *.txt > files.txt
        echo 'qarrayrun SGE_TASK_ID files.txt sort -o sorted.{1} {1}' | qsub -t 1-$(cat files.txt | wc -l) -cwd -j y -V -o log

        # Your input file might have multiple columns, use {2} for the 2nd column
        # Sort the largest files first
        ls *.txt | xargs -n 1 wc -c | sort -n -r > files.txt
        echo 'qarrayrun SGE_TASK_ID files.txt sort -o sorted.{2} {2}' | qsub -t 1-$(cat files.txt | wc -l) -cwd -j y -V -o log

        # Use the --shell option and quote your pipeline when you need shell redirection
        # Remove blanks before sorting files
        ls *.txt > files.txt
        echo 'qarrayrun --shell SGE_TASK_ID files.txt "cat {1} | tr -d [:blank:] | sort > sorted.{1}"' | qsub -t 1-$(cat files.txt | wc -l) -cwd -j y -V -o log
        """)

    formatter_class = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(description=description, epilog=epilog, formatter_class=formatter_class)

    parser.add_argument(dest="subtask_var", type=str, metavar="NAME", help="""Name of the environment variable that contains the sub-task number
                                                                              You should use SGE_TASK_ID with Grid Engine and PBS_ARRAYID with Torque.""")
    parser.add_argument(dest="array_file", type=str, help="""Name of the file containing the arguments for each sub-task with one line
                                                             per sub-task.  This script will extract the arguments for this sub-task
                                                             at the line number identified by the sub-task environment variable
                                                             (SGE_TASK_ID or PBS_ARRAYID).  The line is parsed and substituted
                                                             into the command, replacing the parameter placeholders with the actual
                                                             arguments.""")
    parser.add_argument(dest="command", help="""The remainder of the command line is the command to be executed with parameter
                                                placeholders of the form {1}, {2}, {3} ...""")
    parser.add_argument("--shell", dest="shell", action="store_true", help="Run the command through the shell.")
    parser.add_argument("--version", action="version", version="%(prog)s version " + __version__)

    args, remainder = parser.parse_known_args(system_args)

    return args, remainder


def run_command(args, remainder):
    """Execute a single subtask of an array job.

    Parameters
    ----------
    args : Namespace
        Command line arguments stored as attributes of a Namespace, usually
        parsed from sys.argv
    remainder : list
        List of remaining argument strings
    """
    command = [args.command] + remainder
    command_line = ' '.join(command)
    return qarrayrun.run(args.subtask_var, args.array_file, command_line, args.shell)


def run_command_from_args(args, remainder):
    """Run a command with previously parsed arguments in an argparse namespace.

    This function is intended to be used for unit testing.

    Parameters
    ----------
    args : Namespace
        Command line arguments are stored as attributes of a Namespace.
        The args are obtained by calling parse_argument_list().
    remainder : list
        List of remaining argument strings

    Returns
    -------
    Returns 0 on success if it completes with no exceptions.
    """
    return run_command(args, remainder)


def run_from_line(line):
    """Run a command with a command line.

    This function is intended to be used for unit testing.

    Parameters
    ----------
    line : str
        Command line.

    Returns
    -------
    Returns 0 on success if it completes with no exceptions.
    """
    argv = line.split()
    args, remainder = parse_arguments(argv)
    return run_command(args, remainder)


def main():
    """This is the main function which is turned into an executable
    console script by the setuptools entry_points.  See setup.py.

    To run this function as a script, first install the package:
        $ python setup.py develop
        or
        $ pip install --user qarrayrun

    Parameters
    ----------
    This function must not take any parameters

    Returns
    -------
    The return value is passed to sys.exit().
    """
    enable_log_timestamps = False
    if enable_log_timestamps:
        logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
    else:
        logging.basicConfig(format="%(message)s", level=logging.INFO)
    args, remainder = parse_arguments(sys.argv[1:])
    return run_command(args, remainder)


# This snippet lets you run the cli without installing the entrypoint.
if __name__ == "__main__":
    sys.exit(main())
