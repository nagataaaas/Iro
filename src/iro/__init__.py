"""
    IRO
    ===

    Easy and powerful Colorizer for Python!

    Powered by [Yamato Nagata](https://twitter.com/514YJ)

    [GitHub](https://github.com/nagataaaas/Iro)
    Powered by [Yamato Nagata](https://twitter.com/514YJ)
    [GitHub](https://github.com/nagataaaas/Iro)
    :copyright: (c) 2024 by Yamato Nagata.
    :license: MIT.
"""

import locale

from .__about__ import __version__
from .iro import Iro
from .styles import FGColor, BGColor, ColorRGB, Color256, Font, IroElement, Style

locale.setlocale(locale.LC_ALL, '')

__all__ = [
    "__version__",
    "Iro",
    "FGColor",
    "BGColor",
    "Style",
    "ColorRGB",
    "Color256",
    "Font",
    "IroElement",
]
