#!/bin/sh
HOJE="`date +%Y-%m-%d`"
python orgaos.py | sort | uniq > dados/orgaos-$HOJE.txt
