#!/usr/bin/python3

"""
loads the themes from themes directory, so that themes can be applied
only has to be done when themes are changed
"""
import os
import re
import colorsys


WALLPAPER_DIR = "/mnt/win/Program Files (x86)/Steam/steamapps/workshop/content/431960/"

THEME_DIR = "/home/air_berlin/Theme/"
BLANK_NAME = "blank"
NEEDED_CONFIGS = ["-kitty", "-ncspot", "-waybar-style.css", "-zathurarc", "-left-wallpaper", "-right-wallpaper", "-emacs-theme", "-dark", "-light", "-font", "-discord", "-zathura-reload"]

color_formats={
    "rgba": lambda r, g, b, op : f"rgba({r}, {g}, {b}, {op})",
    "rgb": lambda r, g, b, op : f"rgb({r}, {g}, {b})",
    "hex": lambda r, g, b, op : f"#{to_hex(r):02}{to_hex(g):02}{to_hex(b):02}",
    "hexa": lambda r, g, b, op : f"#{to_hex(r):02}{to_hex(g):02}{to_hex(b):02}{to_hex(op):02})",
    "hexold": lambda r, g, b, op : f"0x{to_hex(op):02}{to_hex(r):02}{to_hex(g):02}{to_hex(b):02}",
    "hlsh": lambda r, g, b, op : f"{colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[0] * 360}",
    "hlss": lambda r, g, b, op : f"{colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[2]}",
    "hlsl": lambda r, g, b, op : f"{colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[1]}",
}


# color_looks_like="color:color_format[:opacity:opacity_value]"


def to_hex(col_val):
    if "." in str(col_val):
        col_val = float(col_val) * 255
    return hex(int(col_val))[2:]


def read_theme(theme_name):
    theme_vals = {}
    with open(f"{THEME_DIR}themes/{theme_name}") as fp:
        lines = fp.readlines()
    for line in lines:
        line = line.split(":")
        for i, l in enumerate(line):
            line[i] = l.strip()
        if line[1][:3] == "rgb":
            colors = line[1].split(",")[1:]
            for i, col in enumerate(colors):
                colors[i] = int(col.strip())
                line[1] = colors
        theme_vals.update({line[0]: line[1]})
    return theme_vals


def read_blank(conf):
    with open(f"{THEME_DIR}{BLANK_NAME}s/{BLANK_NAME}{conf}", "r") as fp:
        return fp.read()


def write_conf(theme_name, conf, content):
    try:
        os.mkdir(f"{THEME_DIR}{theme_name}-theme-dir")
    except OSError:
        pass
    with open(f"{THEME_DIR}{theme_name}-theme-dir/{theme_name}{conf}", "w") as fp:
        return fp.write(content)


def create_config(theme_name, theme_vals):
    for conf in NEEDED_CONFIGS:
        text = read_blank(conf)

        replacing = True
        while replacing:
            if re.search("%%%.*%%%", text) is None:
                break
            to_replace = re.search("%%%.*%%%", text).group()[3:-3]
            # yeah nobody needs this tmp
            text = re.sub("%%%.*%%%", "%%%tmp%%%", text, count=1)
            to_replace = to_replace.split(":")
            if len(to_replace) == 1:
                if "movie" in to_replace[0]:
                    res = WALLPAPER_DIR + theme_vals[to_replace[0]]
                else:
                    res = theme_vals[to_replace[0]]
            if len(to_replace) == 2:
                r = theme_vals[to_replace[0]][0]
                g = theme_vals[to_replace[0]][1]
                b = theme_vals[to_replace[0]][2]
                res = color_formats[to_replace[1]](r, g, b, None)
            if len(to_replace) >= 4:
                r = theme_vals[to_replace[0]][0]
                g = theme_vals[to_replace[0]][1]
                b = theme_vals[to_replace[0]][2]
                res = color_formats[to_replace[1]](r, g, b, to_replace[3])
            text = re.sub("%%%tmp%%%", res, text)
        write_conf(theme_name, conf, text)


def find_all_themes():
    themes = os.listdir(f"{THEME_DIR}themes/")
    with open(f"{THEME_DIR}loaded_themes", "w") as fp:
        for theme in themes:
            fp.write(theme + "\n")
    return themes


def main():
    themes = find_all_themes()
    for theme in themes:
        theme_vals = read_theme(theme)
        create_config(theme, theme_vals)


if __name__ == "__main__":
    main()
