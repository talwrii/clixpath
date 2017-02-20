from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import json
import os.path
import sys

import lxml.etree

if sys.version_info.major == 3:
    unicode = str


def build_parser():
    parser = argparse.ArgumentParser(description='Extract data from an html/xml file using xpath')
    parser.add_argument('--json', '-J', action='store_true', help='Produce output in machine readable json')
    parser.add_argument('xpath', type=str, help='Xpath expression')
    parser.add_argument('file', type=str, nargs='*', help='File to operate on. (Path included in json)')
    return parser

def main():
    result = run(sys.argv[1:], sys.stdin)
    if result is not None:
        for line in result:
            sys.stdout.write(line.encode('utf8'))
            sys.stdout.flush()

def get_element_path(elt):
    items = []
    while elt is not None:
        try:
            tag = elt.tag
        except AttributeError:
            elt = elt.getparent()
            continue

        try:
            attribs = elt.attrib
            shown_attribs = {k:v for (k, v) in attribs.items() if k in ('id', 'class')}
            attrib_text = ' and '.join('@{}="{}"'.format(k, v) for k, v in sorted(shown_attribs.items()))
        except AttributeError:
            attrib_text = None

        if attrib_text:
            items.append('{}[{}]'.format(tag, attrib_text))
        else:
            items.append(tag)

        elt = elt.getparent()
        if elt is None:
            break
    return '/' + '/'.join(reversed(items))

def run(args, input_stream):
    options = build_parser().parse_args(args)
    del args

    if not options.file:
        streams = [('STDIO', input_stream)]
    else:
        streams = [(os.path.abspath(f), open(f)) for f in options.file]

    for path, stream in streams:
        for entry in parse_stream(options.xpath, stream):
            entry['file'] = path
            if options.json:
                yield json.dumps(entry, sort_keys=True) + "\n"
            else:
                yield entry['markup'] + "\n"


def parse_stream(xpath, input_stream):
    tree = lxml.etree.HTML(input_stream.read())
    result = []
    xml_entries = []
    for elt in tree.xpath(xpath):
        path = get_element_path(elt)
        if isinstance(elt, (str, unicode)):
            markup = unicode(elt)
        else:
            markup = lxml.etree.tostring(elt, encoding=unicode)

        yield dict(markup=markup, path=path)

def strip_trailing_whitespace(string):
    return '\n'.join([l.strip() for l in string.splitlines()])
