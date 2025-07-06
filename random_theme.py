#!/usr/bin/python3

"""applies a random theme"""
from subprocess import run
import random
import os
from time import sleep
from sys import argv

themes = []
with open("/home/air_berlin/Theme/loaded_themes", "r") as fp:
    for line in fp.readlines():
        themes.append(line.strip())

with open("/home/air_berlin/Theme/current_theme", "r") as fp:
    cur_theme = fp.read().strip()


if len(argv) > 1:
    sleep(5)
run(["/home/air_berlin/Theme/apply_theme.sh", random.choice(themes)])
#, stdout=open(os.devnull, 'wb'), stderr=open(os.devnull, 'wb'))
