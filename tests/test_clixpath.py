
# -*- coding: utf8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from clixpath.clixpath import run
from io import StringIO


class TestClix(unittest.TestCase):
    def setUp(self):
        self.direc = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.direc)

    def run_cli(self, *args):
        input_string = args[-1]
        return ''.join(run(args[:-1], StringIO(input_string)))

    def test_readme(self):
        HERE = os.path.dirname(__file__) or '.'
        readme = backticks([sys.executable, os.path.join(HERE, '..', 'make-readme.py'), '--stdout'])

        with open(os.path.join(HERE, '..', 'README.md')) as stream:
            readme_file_text = stream.read()

        self.assertEqual(readme_file_text, readme)

    def test_unicode(self):
        TEXT = u'<a>’</a>'
        entry = self.run_cli('//a/text()', TEXT)
        self.assertEqual(entry, "’\n")
        entry = self.run_cli('//a', TEXT)
        self.assertEqual(entry, "<a>’</a>\n")

    def test_basic(self):
        TEXT = '''
        <html>
        <body><a href="blah">hello</a></body>
        </html>
        '''
        entry = json.loads(self.run_cli('//a', '--json', TEXT))
        self.assertEqual(entry['markup'], '<a href="blah">hello</a>')

        entry = json.loads(self.run_cli('//a/@href', '--json', TEXT))
        self.assertEqual(entry['markup'], 'blah')

        self.run_cli('//a', TEXT)

def backticks(command, stdin=None, shell=False):
    stdin_arg = subprocess.PIPE if stdin is not None else None

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=stdin_arg, shell=shell)
    result, _ = process.communicate(stdin)
    result = result.decode('utf8')
    if process.returncode != 0:
        raise Exception('{!r} returned non-zero return code {!r}'.format(command, process.returncode))
    return result


if __name__ == '__main__':
    unittest.main()
