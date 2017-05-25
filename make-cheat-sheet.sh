#!/bin/bash
set -o errexit

function echo_run {
    echo "\$ $1"

    # LIES!
    # This allows me to use this code for testing with
    #   python 2 and python3
    # whilst also producing documentation
    #   combining documentation with testing has a lot of
    #   benefits

    command=$(echo $1 | sed "s_clixpath_$python -m clixpath_")
    eval "$command"
}


python=${PYTHON:-python}


echo '#Basic usage'
echo_run "curl -L --silent http://xkcd.com/1833 | clixpath '//img/@src'"
echo
echo
echo '#Machine readable output (the main reason for this tool)'
echo_run "curl -L --silent http://xkcd.com/1833 | clixpath --json '//img'"
echo
echo
echo '#Extracting structured data from records (like capture groups in regexp)'
echo_run "curl -L --silent http://xkcd.com/1833 | clixpath '//img' --extract alt_text @alt --extract source @src"
