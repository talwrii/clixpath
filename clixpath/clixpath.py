from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import json
import os.path
import sys
import io

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
    sys.stdout = io.open(sys.stdout.fileno(), 'w', encoding='utf8')
    result = run(sys.argv[1:], sys.stdin)
    if result is not None:
        for line in result:
            sys.stdout.write(line)
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

            key_values = extract_key_values(options.extract, entry)

            if options.json:
                yield format_json_entry(entry, key_values, options.no_key)
            elif key_values:
                values = [pair[0] + ':' + (pair[1] or '') for pair in sorted(key_values.items())]
                yield entry['markup'].rstrip() + '\n'  + '\n'.join(values) + '\n\n'
            else:
                yield entry['markup'] + '\n'

def format_json_entry(entry, key_values, dropped_keys):
    entry = dict(entry, **key_values)
    del entry['tree']
    if dropped_keys:
        for key in dropped_keys:
            del entry[key]
    return json.dumps(entry, sort_keys=True) + "\n"

def extract_key_values(xpaths, entry):
    key_values = dict()
    if xpaths:
        for key, xpath in xpaths:
            values = entry['tree'].xpath(xpath)
            if len(values) == 1:
                values, = values
            elif len(values) == 0:
                values = None
            key_values[key] = values
    return key_values


def parse_stream(xpath, input_stream, drop):
    tree = lxml.etree.HTML(input_stream.read())
    result = []
    xml_entries = []
    for elt in tree.xpath(xpath):
        for drop_path in drop:
            delete_xpath(elt, drop_path)

        path = get_element_path(elt)

        if isinstance(elt, (str, unicode)):
            markup = unicode(elt)
        else:
            markup = lxml.etree.tostring(elt, encoding=unicode)

        yield dict(markup=markup, path=path, tree=elt)

def delete_xpath(elt, drop_path):
    while True:
        # avoid deleting something we have already deleted
        to_drop = elt.xpath(drop_path)
        if not to_drop:
            break
        to_drop[0].getparent().remove(to_drop[0])

def strip_trailing_whitespace(string):
    return '\n'.join([l.strip() for l in string.splitlines()])
