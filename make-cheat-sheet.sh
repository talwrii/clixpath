#!/bin/bash
set -o errexit

function echo_run {
    echo "\$ $1"
    eval "$1"
}

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
