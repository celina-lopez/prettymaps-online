#!/usr/bin/env python3

# import vsketch
from .prettymaps import *
import matplotlib.font_manager as fm
from matplotlib import pyplot as plt
from PIL import Image
import numpy
from io import BytesIO
import base64

theme = {
    0: {
        'background': {'fc': '#FFDEDE', 'ec': '#FFDEDE', 'hatch': 'ooo...', 'zorder': -1},
        'perimeter': {'fill': False, 'lw': 0, 'zorder': 0},
        'green': {'fc': '#CAF7E3', 'ec': '#95E1D3', 'hatch_c': '#A7C497', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
        'water': {'fc': '#a8e1e6', 'ec': '#2F3737', 'hatch_c': '#9bc3d4', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
        'streets': {'fc': '#4A1C40', 'ec': '#480032', 'alpha': 1, 'lw': 0, 'zorder': 4},
        'building': {'palette': ['#BEAEE2', '#F6C6EA'], 'ec': '#480032', 'lw': .5, 'zorder': 5},
    },
    1: {
        'background': {'fc': '#FCF0C8', 'ec': '#FCF0C8', 'hatch': 'ooo...', 'zorder': -1},
        'perimeter': {'fill': False, 'lw': 0, 'zorder': 0},
        'green': {'fc': '#CEE5D0', 'ec': '#7EB5A6', 'hatch_c': '#A7C497', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
        'water': {'fc': '#a8e1e6', 'ec': '#2F3737', 'hatch_c': '#9bc3d4', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
        'streets': {'fc': '#86340A', 'ec': '#86340A', 'alpha': 1, 'lw': 0, 'zorder': 4},
        'building': {'palette': ['#630A10', '#F0A500'], 'ec': '#480032', 'lw': .5, 'zorder': 5},
    },
    2: {
        'background': {'fc': '#E4FBFF', 'ec': '#E4FBFF', 'hatch': 'ooo...', 'zorder': -1},
        'perimeter': {'fill': False, 'lw': 0, 'zorder': 0},
        'green': {'fc': '#CCFFBD', 'ec': '#7ECA9C', 'hatch_c': '#A7C497', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
        'water': {'fc': '#a8e1e6', 'ec': '#2F3737', 'hatch_c': '#9bc3d4', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
        'streets': {'fc': '#C400FF', 'ec': '#FF67E7', 'alpha': 1, 'lw': 0, 'zorder': 4},
        'building': {'palette': ['#7C83FD', '#78DEC7'], 'ec': '#480032', 'lw': .5, 'zorder': 5},
    },
    3: {
        'background': {'fc': '#F2F4CB', 'ec': '#F2F4CB', 'hatch': 'ooo...', 'zorder': -1},
        'perimeter': {'fill': False, 'lw': 0, 'zorder': 0},
          'green': {'fc': '#8BB174', 'ec': '#2F3737', 'hatch_c': '#A7C497', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
        'water': {'fc': '#a8e1e6', 'ec': '#2F3737', 'hatch_c': '#9bc3d4', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
        'streets': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 4},
        'building': {'palette': ['#433633', '#FF5E5B'], 'ec': '#2F3737', 'lw': .5, 'zorder': 5},
    },
    4: {
        'background': {'fc': '#FFE194', 'ec': '#FFE194', 'hatch': 'ooo...', 'zorder': -1},
        'perimeter': {'fill': False, 'lw': 0, 'zorder': 0},
        'green': {'fc': '#CAF7E3', 'ec': '#95E1D3', 'hatch_c': '#A7C497', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
        'water': {'fc': '#a8e1e6', 'ec': '#2F3737', 'hatch_c': '#9bc3d4', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
        'streets': {'fc': '#FFB830', 'ec': '#DF711B', 'alpha': 1, 'lw': 0, 'zorder': 4},
        'building': {'palette': ['#A3A847', '#7F8B52'], 'ec': '#480032', 'lw': .5, 'zorder': 5},
    },
    5: {
        'background': {'fc': '#F0D9FF', 'ec': '#F0D9FF', 'hatch': 'ooo...', 'zorder': -1},
        'perimeter': {'fill': False, 'lw': 0, 'zorder': 0},
        'green': {'fc': '#FFC107', 'ec': '#FFED99', 'hatch_c': '#A7C497', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
        'water': {'fc': '#a8e1e6', 'ec': '#2F3737', 'hatch_c': '#9bc3d4', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
        'streets': {'fc': '#FF5E78', 'ec': '#EB596E', 'alpha': 1, 'lw': 0, 'zorder': 4},
        'building': {'palette': ['#3C5186', '#9B72AA'], 'ec': '#726A95', 'lw': .5, 'zorder': 5},
    }
}

def get_image(x, y, name, theme_num):
    dilate = 100
    # Setup figure
    fig, ax = plt.subplots(figsize = (10, 10), constrained_layout = True)

    # Plot
    layers = plot(
        (x , y), radius = 100,
        ax = ax,
        layers = {
            'perimeter': {'circle': False, 'dilate': dilate},
            'streets': {
                'width': {
                    'primary': 5,
                    'secondary': 4,
                    'tertiary': 3,
                    'residential': 2,
                    'footway': 1,
                },
                'circle': False,
                'dilate': dilate
            },
            'building': {
                'tags': {'building': True},
                'union': False,
                'circle': False,
                'dilate': dilate
            },
            'green': {
                'tags': {
                    'landuse': ['grass', 'village_green'],
                    'leisure': 'park'
                },
                'circle': False,
                'dilate': dilate
            },
        },
        drawing_kwargs = theme[theme_num],
        osm_credit = {'x': 0, 'y': 0, 'color': '#fff'}
    )

    # Set bounds
    xmin, ymin, xmax, ymax = layers['perimeter'].bounds
    dx, dy = xmax-xmin, ymax-ymin
    ax.set_xlim(xmin-.06*dx, xmax+.06*dx)
    ax.set_ylim(ymin-.06*dy, ymax+.06*dy)

    # Draw left text
    ax.text(
        xmin-.06*dx, ymin+.5*dy,
        name,
        color = '#2F3737',
        rotation = 90,
        fontproperties = fm.FontProperties(fname = './services/PermanentMarker-Regular.ttf', size = 35),
    )

    image = BytesIO()
    plt.savefig(image, format='png')
    image.seek(0)
    image_string = base64.b64encode(image.read())

    return image_string.decode('utf8')

    # plt.savefig('./prints/yakiniq.png')
    # # plt.savefig('./prints/yakiniq.svg')

    # im = Image.open("./prints/yakiniq.png")
    # im1 = im.crop((147, 101, 980, 980))
    # im1.save("./prints/yakiniq.png")

