#!/usr/bin/python3

"""cycles to the next theme"""
from subprocess import call

themes = []
with open("/home/air_berlin/Theme/loaded_themes", "r") as fp:
    for line in fp.readlines():
        themes.append(line.strip())

with open("/home/air_berlin/Theme/current_theme", "r") as fp:
    cur_theme = fp.read().strip()

curi = themes.index(cur_theme)
if curi == len(themes) - 1:
    i = 0
else:
    i = curi + 1

call(["/home/air_berlin/Theme/apply_theme.sh", themes[i]])
