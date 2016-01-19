python-fedex Examples
=====================

This directory contains a number of examples of how to use python-fedex. For
these examples to work, you must open example_config.py and enter your
testing account credentials there.

To run all tests from bash, type:

    for f in *.py; do python "$f"; done
    # Or use the below to only see response errors:
    for f in *.py; do python "$f"; done | grep -i error