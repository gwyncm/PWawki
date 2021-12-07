#! /bin/bash
#
# Wawki cgi control script version 1.1 Copyright Gwyneth Morrison
#
echo "Content-type: text/html"
echo
echo
export CGI=YES
./wawki $*
