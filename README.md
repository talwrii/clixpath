<!-- This is generated by make-readme.py do not edit -->
# clixpath

A command-line tool to extract the values of *Xpath* expressions from *HTML* and *XML* documents.
clixpath's distinguishing features are intended ease of use and producing output that can be parsed
programmatically.
Supports value extraction analogous to captuure groups in regexp.

A companion utility to [clixmod](https://github.com/talwrii/clixmod).

Tested with Python 2.7 and Python 3.5.

# Installing

```
pip install git+https://github.com/talwrii/clixpath#egg=clixpath
```

# Related tools (and flagrant self-promotion)

The author maintains a [list of some tools he has written](https://github.com/talwrii/tools).

# Examples / Cheat sheet

```bash
#Basic usage
$ curl -L --silent http://xkcd.com/1833 | clixpath '//img/@src'
/s/0b7742.png
//imgs.xkcd.com/comics/code_quality_3.png
//imgs.xkcd.com/s/a899e84.jpg
//imgs.xkcd.com/s/temperature.png


#Machine readable output (the main reason for this tool)
$ curl -L --silent http://xkcd.com/1833 | clixpath --json '//img'
{"file": "STDIO", "markup": "<img src=\"/s/0b7742.png\" alt=\"xkcd.com logo\" height=\"83\" width=\"185\"/>", "path": "/html/body/div[@id=\"topContainer\"]/div[@id=\"topRight\"]/div[@id=\"masthead\"]/span/a/img"}
{"file": "STDIO", "markup": "<img src=\"//imgs.xkcd.com/comics/code_quality_3.png\" title=\"It's like a half-solved cryptogram where the solution is a piece of FORTH code written by someone who doesn't know FORTH.\" alt=\"Code Quality 3\" srcset=\"//imgs.xkcd.com/comics/code_quality_3_2x.png 2x\"/>\n", "path": "/html/body/div[@class=\"box\" and @id=\"middleContainer\"]/div[@id=\"comic\"]/img"}
{"file": "STDIO", "markup": "<img src=\"//imgs.xkcd.com/s/a899e84.jpg\" width=\"520\" height=\"100\" alt=\"Selected Comics\" usemap=\"#comicmap\"/>\n", "path": "/html/body/div[@class=\"box\" and @id=\"bottom\"]/img"}
{"file": "STDIO", "markup": "<img border=\"0\" src=\"//imgs.xkcd.com/s/temperature.png\" width=\"520\" height=\"100\" alt=\"Earth temperature timeline\"/>", "path": "/html/body/div[@class=\"box\" and @id=\"bottom\"]/a/img"}


#Extracting structured data from records (like capture groups in regexp)
$ curl -L --silent http://xkcd.com/1833 | clixpath '//img' --extract alt_text @alt --extract source @src
<img src="/s/0b7742.png" alt="xkcd.com logo" height="83" width="185"/>
alt_text:xkcd.com logo
source:/s/0b7742.png

<img src="//imgs.xkcd.com/comics/code_quality_3.png" title="It's like a half-solved cryptogram where the solution is a piece of FORTH code written by someone who doesn't know FORTH." alt="Code Quality 3" srcset="//imgs.xkcd.com/comics/code_quality_3_2x.png 2x"/>
alt_text:Code Quality 3
source://imgs.xkcd.com/comics/code_quality_3.png

<img src="//imgs.xkcd.com/s/a899e84.jpg" width="520" height="100" alt="Selected Comics" usemap="#comicmap"/>
alt_text:Selected Comics
source://imgs.xkcd.com/s/a899e84.jpg

<img border="0" src="//imgs.xkcd.com/s/temperature.png" width="520" height="100" alt="Earth temperature timeline"/>
alt_text:Earth temperature timeline
source://imgs.xkcd.com/s/temperature.png


```

# Usage

```
usage: clixpath [-h] [--debug] [--json] [--drop DROP] [--extract KEY VALUE]
                [--no-key NO_KEY]
                xpath [file [file ...]]

Extract data from an html/xml file using xpath

positional arguments:
  xpath                 Xpath expression
  file                  File to operate on. (Path included in json)

optional arguments:
  -h, --help            show this help message and exit
  --debug               Include debug output (to stderr)
  --json, -J            Produce output in machine readable json
  --drop DROP, -d DROP  Delete xpaths from result
  --extract KEY VALUE, -x KEY VALUE
                        Takes args KEY XPATH and extact XPATH from matches and
                        stores in in KEY
  --no-key NO_KEY, -n NO_KEY
                        Do not include this item in output. (E.g. markup)

```
# Alternatives considered before writing

- **xmlstarlet** I always forget how this works and I couldn't make it like HTML with 5 minutes work
- **xmllint**  Easy to use, but I could not make the output easily parseable
- **xidel** Considered, but I doubted it would produce machine readable output, and it was in pascal
- **pq** Did not produce machine readable output
- **htmlpath** Did not produce machine readable output, project seemed too small to justify taking up the authors time pushing changes
- **cli-scrape**  Didn't run when I used it, gave up after 5 minutes (sorry for the FUD)
- **XSLT** useful for more general tasks, boilerplate plus learning curve
- **lxml in python** mostly the same as xslt with a slightly more shallow learning curve at the price of requiring turing completeness.
- **Converting your XML / HTML into json** you can then use JSON tools like *jq*. See, for example, [xml2json](https://github.com/hay/xml2json). I found this approach problematic when using XML with namespaces.
- **XPath 2.0** and **XQuery** support [some transformation of data](https://stackoverflow.com/questions/11372160/how-to-do-group-capture-in-xpath) that could be used for this sort of task, albeit with some boiler plate. A cursory inspection of open source tools failed to find any tools that I would describe as "do what I mean convenient command line tools". Though the reader might like to be aware of [xqilla](http://xqilla.sourceforge.net/) and [galax](http://galax.sourceforge.net/)

# Testing

- If you write tests in the `tests` directory, then I will trust you code more.
- If you run tox then it will work when I run it before merging your code...

# Caveats

This tool is in the category of convenience utilities rather than a general-purpose tool.
It makes common tasks easy and general tasks impossible.

I may not accept your patch on the grounds of something being too complicated for this tool.
The most likely place that this will come up is support for building recursive *JSON* records using the `--extract` option.

In such cases, a more powerful tool like *XSLT* or *lxml* should be used.

Do not expect any code that depends on parsing *non*-JSON output to not getting broken.
