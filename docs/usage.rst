========
Usage
========

.. highlight:: bash

Quick test
----------

To try qarrayrun::

  # Create a file with array job parameters, one line per task.
  $ echo A B C > file
  $ echo X Y Z >> file

  # Store the task number in an envirnment variable.
  # Normally, this is done automatically by the HPC job execution engine.
  $ export SGE_TASK_ID=1

  # Execute qarrayrun
  $ qarrayrun SGE_TASK_ID file "echo {3} {2} {1}"
  C B A

  # Repeat for task 2
  $ export SGE_TASK_ID=2
  $ qarrayrun SGE_TASK_ID file "echo {3} {2} {1}"
  Z Y X

  # You can reuse any parameter more than once and create more complex command lines
  $ qarrayrun SGE_TASK_ID file "echo {1}/{1}/{2}.{2}/{3}{3}.txt"
  X/X/Y.Y/ZZ.txt


Use with qsub
-------------

To use qarrayrun with qsub, pipe the qarrayrun command line into qsub, and tell qsub how many tasks are in the job.
The HPC job execution engine will automatically set the task number in an environment variable and execute qarrayrun
on compute nodes.

Follow these examples::

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

Language
--------

As you can see from the examples above, qarrayrun has a very simple language for extracting parameters
from a file and substituting the parameters into a command line.

Parameters in the array job parameter file are whitespace-separated.  The parameters can have any meaning
you want -- numbers, strings, file names, directory names, etc.

The substitution language is just a number inside curly braces.

``{1}`` is the first parameter found in the array job parameter file.

``{2}`` is the second parameter found in the array job parameter file.

``{3}`` is the third parameter found in the array job parameter file.

``{1000}`` is the 1000th parameter found in the array job parameter file.  There is no limit to the
number of parameters per line in the array job parameter file.


Variable number of parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes, the lines in the array job parameter file may have varying numbers of parameters.  If you specify
a substitution placeholder with a parameter number higher than the number of parameters on the line, it will
be silently ignored and replaced by an empty string.  This lets you pass a variable number of parameters to
other programs.
