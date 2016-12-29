# make code as python 3 compatible as possible
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import shutil
import StringIO
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

if __name__ == '__main__':
    unittest.main()
