from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import json
import sys

import lxml.etree

if sys.version_info.major == 3:
    unicode = str


def build_parser():
    parser = argparse.ArgumentParser(description='Extract data from an html/xml file using xpath')
    parser.add_argument('--json', '-J', action='store_true', help='Produce output in machine readable json')
    parser.add_argument('xpath', type=str, help='Xpath expression')
    return parser

def main():
    result = run(sys.argv[1:], sys.stdin)
    if result is not None:
        print(result.encode('utf8'))
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
    tree = lxml.etree.HTML(input_stream.read())
    result = []
    xml_entries = []
    for elt in tree.xpath(options.xpath):
        path = get_element_path(elt)
        if isinstance(elt, (str, unicode)):
            markup = unicode(elt)
        else:
            markup = lxml.etree.tostring(elt, encoding=unicode)

        result.append(markup)
        xml_entries.append(dict(markup=markup, path=path))
    if options.json:
        return strip_failing_whitespace(json.dumps(xml_entries, indent=4, sort_keys=True))
    else:
        return '\n'.join(result)

def strip_failing_whitespace(string):
    return '\n'.join([l.strip() for l in string.splitlines()])
