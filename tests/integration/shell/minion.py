# -*- coding: utf-8 -*-
"""
    tests.integration.shell.minion
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: © 2012 UfSoft.org - :email:`Pedro Algarvio (pedro@algarvio.me)`
    :license: Apache 2.0, see LICENSE for more details.
"""

import sys

# Import salt libs
from saltunittest import TestLoader, TextTestRunner
import integration
from integration import TestDaemon


class MinionTest(integration.ShellCase, integration.ShellCaseCommonTestsMixIn):

    _call_binary_ = 'salt-minion'

if __name__ == "__main__":
    loader = TestLoader()
    tests = loader.loadTestsFromTestCase(MinionTest)
    print('Setting up Salt daemons to execute tests')
    with TestDaemon():
        runner = TextTestRunner(verbosity=1).run(tests)
        sys.exit(runner.wasSuccessful())