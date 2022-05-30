#!/usr/bin/env python3
"""Matplotlib themes as dictionaries."""

from typing import List
import matplotlib as mpl
import matplotlib.pyplot as plt

# Colors are taken from BlueprintJS. Background-foreground colors are default in Elastic UI.

rho = {
    # text sizes
    "axes.labelsize": "large",
    "axes.titlesize": "x-large",
    "figure.titlesize": "xx-large",
    # text weights
    "axes.titleweight": 400,
    "figure.titleweight": 700,
    # if grid is turned on, have it go below plots
    "axes.axisbelow": "false",
    "grid.linestyle": "-",
    "grid.linewidth": 1.0,
    # turn off grid by default
    "axes.grid": "false",
    # turn off ticks on axes
    "xtick.major.size": 0,
    "xtick.minor.size": 0,
    "ytick.major.size": 0,
    "ytick.minor.size": 0,
    # sans-serif by default
    "font.family": "sans-serif",
    # use Computer Modern for LaTeX
    "mathtext.fontset": "cm",
    # turn off right and top spines
    "axes.spines.right": "false",
    "axes.spines.top": "false",
    # set default figure size to a bit more than 6.4 x 4.8
    "figure.figsize": (8, 6),
}


rho_light = rho.copy()
rho_dark = rho.copy()

# colors from https://blueprintjs.com/docs/#core/colors

# intended to approximate the standard ordering found in cat10 or similar. For
# my purposes, it's rare that you're using all of them and that you need maximum
# visual clarity. What's more common is using a couple colors or using them
# redundantly. If you want maximum discernability, use Glasbey from colorcet.

# An example of this tradeoff: blue and orange are the easiest pair to tell
# apart, which is why you see them in Rocket League or Splatoon or similar games
# with teams. But blue and green look much nicer as the only two colors in a
# plot, and they're still discernible with most forms of colorblindness. So blue
# and green are the first pair, and then orange is the third color.

rho_light["axes.prop_cycle"] = mpl.cycler(
    color=[
        "147EB3",
        "29A634",
        "D1980B",
        "D33D17",
        "9D3F9D",
        "00A396",
        "DB2C6F",
        "8EB125",
        "946638",
        "7961DB",
    ]
)

rho_dark["axes.prop_cycle"] = mpl.cycler(
    color=[
        "4C72B0",
        "DD8452",
        "55A868",
        "C44E52",
        "8172B3",
        "937860",
        "DA8BC3",
        "8C8C8C",
        "CCB974",
        "64B5CD",
    ]
)

# the neutrals are from https://elastic.github.io/eui/#/theming/colors
# the naming is from a light-scheme perspective

light_shades = [
    # empty shade: primary background
    "FFFFFF",
    # lightest shade: secondary background
    "F0F4FB",
    # light shade: borders and dividers
    "D3DAE6",
    # medium shade: subdued text
    "98A2B3",
    # dark shade: secondary foreground
    "69707D",
    # darkest shade: primary foreground, text
    "343741",
]

dark_shades = [
    # empty shade: primary background
    "1D1E24",
    # lightest shade: secondary background
    "25262E",
    # light shade: borders and dividers
    "343741",
    # medium shade: subdued text
    "535966",
    # dark shade: secondary foreground
    "98A2B3",
    # darkest shade: primary foreground, text
    "D4DAE5",
]

for rc, shades in [(rho_light, light_shades), (rho_dark, dark_shades)]:
    empty, lightest, light, medium, dark, darkest = shades
    rc["axes.facecolor"] = empty
    rc["figure.facecolor"] = empty
    rc["savefig.facecolor"] = empty

    rc["axes.edgecolor"] = light
    rc["figure.edgecolor"] = light
    rc["savefig.edgecolor"] = light

    rc["xtick.color"] = medium
    rc["ytick.color"] = medium

    rc["xtick.labelcolor"] = dark
    rc["ytick.labelcolor"] = dark

    rc["axes.labelcolor"] = darkest
    rc["axes.titlecolor"] = darkest


def setup(is_dark: bool) -> List[str]:
    """Sets up Matplotlib according to the given color scheme. Returns a list of the plot colors."""
    plt.style.use(rho_dark if is_dark else rho_light)
    return plt.rcParams["axes.prop_cycle"].by_key()["color"]
