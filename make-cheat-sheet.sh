#!/bin/bash
set -o errexit

function echo_run {
    echo "\$ $1"
    eval "$1"
}

echo_run "curl --silent http://xkcd.com | clixpath '//img/@src'"
echo
echo
echo_run "curl --silent http://xkcd.com | clixpath --json '//img'"
