#!/usr/bin/env python
"""
This module is used to run the test suite in its entirety. Make sure to run
this before any release and after patch submissions.
"""
import unittest
from tests import t_ship_service

# A list of the modules under the tests package that should be ran.
test_modules = [t_ship_service]

# Fire off all of the tests.
for mod in test_modules:
    suite = unittest.TestLoader().loadTestsFromModule(mod)
    unittest.TextTestRunner(verbosity=2).run(suite)