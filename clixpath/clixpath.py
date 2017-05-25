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
    parser.add_argument('--drop', '-d', type=str, action='append', help='Delete xpaths from result')
    parser.add_argument('--extract', '-x', type=str, action='append', nargs=2, help='Takes args KEY XPATH and extact XPATH from matches and stores in in KEY')
    parser.add_argument('--no-key', '-n', type=str, action='append', help='Remove this key from json output')
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
        for entry in parse_stream(options.xpath, stream, options.drop or []):
            entry['file'] = path

            key_values = dict()
            if options.extract:
                for key, xpath in options.extract:
                    values = entry['tree'].xpath(xpath)
                    if len(values) == 1:
                        values, = values
                    elif len(values) == 0:
                        values = None
                    key_values[key] = values

            if options.json:
                entry = dict(entry, **key_values)
                del entry['tree']

                if options.no_key:
                    for key in options.no_key:
                        del entry[key]

                yield json.dumps(entry, sort_keys=True) + "\n"
            else:
                yield entry['markup'] + "\n"


def parse_stream(xpath, input_stream):
    tree = lxml.etree.HTML(input_stream.read())
    result = []
    xml_entries = []
    for elt in tree.xpath(xpath):
        for drop_path in drop:
            while True:
                # avoid deleting something we have already deleted
                to_drop = elt.xpath(drop_path)
                if not to_drop:
                    break
                to_drop[0].getparent().remove(to_drop[0])

        path = get_element_path(elt)
        if isinstance(elt, (str, unicode)):
            markup = unicode(elt)
        else:
            markup = lxml.etree.tostring(elt, encoding=unicode)

        yield dict(markup=markup, path=path)

def strip_trailing_whitespace(string):
    return '\n'.join([l.strip() for l in string.splitlines()])
