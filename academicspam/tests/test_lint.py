"""Tests that lint python conventions are followed throughout the codebase"""

from pylint import epylint as lint

from django.test import TestCase
from django.conf import settings

###############################################################################
class AutoLintTests(TestCase):
    """Python convention lint test class"""

    def test_pylint_check(self):
        """
        Use pylint to check ID codes from pylint features

        List of codes: http://docs.pylint.org/features.html
        """

        test_modules = ' '.join([settings.PROJECT_ROOT + mod for mod in\
            ['/apps', '/academicspam']])
        check_codes = ','.join(['W0401', 'W0611']) #'C0103' Names

        # Call pylint
        command = '--reports=n --disable=all --ignore=migrations\
                                --enable={checker} {modules}'.format(
            modules=test_modules,
            checker=check_codes
            )

        # command = '--reports=n --ignore=migrations {modules}'.format(
        #     modules=test_modules,
        #     checker=check_codes
        #     )

        # Run pylint, get results, returns (pylint_sdout, pylint_sderr)
        lint_sdout = lint.py_run(command, return_std=True, script='pylint')[0]

        pylintlog = lint_sdout.read()
        self.assertTrue(pylintlog == '', 'PyLint Log not empty\n' + pylintlog)
