from pylint import epylint as lint

from django.test import TestCase
from django.conf import settings

class AutoLintTests(TestCase):
        
    def test_pylint_check(self):
        """
        Use pylint to check ID codes from pylint features

        List of codes: http://docs.pylint.org/features.html
        """
        
        TEST_MODULES = ' '.join([settings.PROJECT_ROOT + mod for mod in ['/apps', '/academicspam']])
        CHECK_CODES = ','.join(['W0401', 'W0611']) # Check names 'C0103'
        
        # Call pylint
        command = '--reports=n --disable=all --ignore=migrations --enable={checker} {modules}'.format(
            modules=TEST_MODULES,
            checker=CHECK_CODES
            )

        # Run pylint, get results
        (pylint_sdout, pylint_sderr) = lint.py_run(command, return_std=True, script='pylint')
                
        pylint_log = pylint_sdout.read()
        self.assertTrue(pylint_log == '', 'PyLint Log not empty\n' + pylint_log)
