"""
    Powered by [Yamato Nagata](https://twitter.com/514YJ)
    [GitHub](https://github.com/nagataaaas/Iro)
    :copyright: (c) 2021 by Yamato Nagata.
    :license: MIT.
"""

import locale

from .__about__ import __version__
from .iro import (Iro, Color, Style, ColorRGB, Color256, Font)


locale.setlocale(locale.LC_ALL, '')

__all__ = [
    "__version__",
    "Iro",
    "Color",
    "Style",
    "ColorRGB",
    "Color256",
    "Font",
]