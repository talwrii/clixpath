<!-- This is generated by make-readme.py do not edit -->
# clixpath

A command-line tool to extract xpath expressions from HTML and XML documents.
It's distinguishing features are intended ease of use, and
producing output that can be parsed programmatically.

Tested with Python 2.7 and Python 3.5.

# Installing

```
pip install git+https://github.com/talwrii/clixpath#egg=MyProject
```

# Testing

- If you write tests in the `tests` directory, then I will trust you code more.
- If you run tox then it will work when I run it before merging your code...

# Examples / Cheat sheet

```bash
$ curl --silent http://xkcd.com | clixpath '//img/@src'
//imgs.xkcd.com/static/terrible_small_logo.png
//imgs.xkcd.com/store/new-xkcd-shirts.png
//imgs.xkcd.com/comics/interest_timescales.png
//imgs.xkcd.com/s/a899e84.jpg


$ curl --silent http://xkcd.com | clixpath --json '//img'
[
{
"markup": "<img src=\"//imgs.xkcd.com/static/terrible_small_logo.png\" alt=\"xkcd.com logo\" height=\"83\" width=\"185\"/>",
"path": "/html/body/div[@id=\"topContainer\"]/div[@id=\"topRight\"]/div[@id=\"masthead\"]/span/a/img"
},
{
"markup": "<img border=\"0\" src=\"//imgs.xkcd.com/store/new-xkcd-shirts.png\"/>",
"path": "/html/body/div[@id=\"topContainer\"]/div[@id=\"topRight\"]/div[@id=\"news\"]/a/img"
},
{
"markup": "<img src=\"//imgs.xkcd.com/comics/interest_timescales.png\" title=\"Sometimes, parts of a slowly-rising mountain suddenly rises REALLY fast, which is extra interesting.\" alt=\"Interest Timescales\"/>\n",
"path": "/html/body/div[@class=\"box\" and @id=\"middleContainer\"]/div[@id=\"comic\"]/img"
},
{
"markup": "<img src=\"//imgs.xkcd.com/s/a899e84.jpg\" width=\"520\" height=\"100\" alt=\"Selected Comics\" usemap=\"#comicmap\"/>\n",
"path": "/html/body/div[@class=\"box\" and @id=\"bottom\"]/img"
}
]

```

# Usage

```
usage: make-readme.py [-h] [--json] xpath

Extract data from an html/xml file using xpath

positional arguments:
  xpath       Xpath expression

optional arguments:
  -h, --help  show this help message and exit
  --json, -J  Produce output in machine readable json

```
# Alternatives considered before writing

- **xmlstarlet** I always forget how this works, and I couldn't make it like HTML with 5 minutes work
- **xmllint**  Easy to use, but I could not make the output easily parseable
- **xidel** Considered, but I doubted it would produce machine readable output, and it was in pascal
- **pq** Did not produce machine readable output
- **htmlpath** Did not produce machine readable output, project seemed too small to justify taking up the authors time pushing changes
- **cli-scrape**  Didn't run when I used it, gave up after 5 minutes (sorry for the FUD)


