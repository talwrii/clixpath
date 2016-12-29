# make code as python 3 compatible as possible
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import os
import shutil
import StringIO
import subprocess
import sys
import tempfile
import unittest

from clixpath.clixpath import run


class TestClix(unittest.TestCase):
    def setUp(self):
        self.direc = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.direc)

    def run_cli(self, *args):
        input_string = args[-1]
        return run(args[:-1], StringIO.StringIO(input_string))

    def test_readme(self):
        HERE = os.path.dirname(__file__) or '.'
        readme = backticks([sys.executable, os.path.join(HERE, '..', 'make-readme.py'), '--stdout'])
        with open(os.path.join(HERE, '..', 'README.md')) as stream:
            readme_file_text = stream.read()
        self.assertEquals(readme_file_text.strip('\n'), readme.strip('\n'))

    def test_basic(self):
        TEXT = '''
        <html>
        <body><a href="blah">hello</a></body>
        </html>
        '''
        entry, = json.loads(self.run_cli('//a', '--json', TEXT))
        self.assertEquals(entry['markup'], '<a href="blah">hello</a>')

        entry, = json.loads(self.run_cli('//a/@href', '--json', TEXT))
        self.assertEquals(entry['markup'], 'blah')

        self.run_cli('//a', TEXT)

def backticks(command, stdin=None, shell=False):
    stdin_arg = subprocess.PIPE if stdin is not None else None

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=stdin_arg, shell=shell)
    result, _ = process.communicate(stdin)
    if process.returncode != 0:
        raise Exception('{!r} returned non-zero return code {!r}'.format(command, process.returncode))
    return result


if __name__ == '__main__':
    unittest.main()
