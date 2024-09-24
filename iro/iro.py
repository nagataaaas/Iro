import math
from abc import abstractmethod
from enum import Enum
from typing import Iterable, List
from warnings import warn


class IroElement:
    @abstractmethod
    def open(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> str:
        raise NotImplementedError


class Iro:
    def __init__(self, *text: Iterable, disable_rgb: bool = True, optimize_level: int = 0):
        self.disable_rgb = disable_rgb
        self.optimize_level = optimize_level

        self.text = self.painter(text) + Style.RESET.open()

    def painter(self, texts: Iterable, given_style=None):
        if self.optimize_level == 0:
            return self.unoptimized_paint(texts, given_style)
        elif self.optimize_level == 1:
            return self.optimized_paint(texts, given_style)
        raise ValueError("optimize_level must be 0 or 1.")

    def unoptimized_paint(self, texts: Iterable, given_style=None):
        if given_style is None:
            style = []
        else:
            style = given_style[:]
        result = []
        text_pool = []

        for elem in texts:
            if isinstance(elem, IroElement):
                style.append(elem)
            else:
                text_pool.append(elem)

        open_style = self.open_styles(style)

        result.append(open_style)

        for text in text_pool:
            if isinstance(text, str):
                result.append(text)
            elif isinstance(text, Iro):
                result.append(text.text)
            else:
                result.append(self.painter(text, style))
                result.append(open_style)

        result.append(self.close_styles(style))

        return ''.join(result)

    def optimized_paint(self, texts: Iterable, given_style=None):
        if given_style is None:
            """
            1: font, 
            2: intensity, (bold, dim)
            3: italic,
            4: underline,
            5: blink,
            6: invert,
            7: hide,
            8: strike,
            9: overline,
            10: fg_color, 
            11: bg_color
            """
            given_style = [None] * 11
            style = [None] * 11
        else:
            style = given_style[:]
        result = []
        text_pool = []

        for elem in texts:
            if isinstance(elem, IroElement):
                if isinstance(elem, Font):  # FONT
                    if elem.font_number == 0:
                        style[0] = None
                        continue
                    style[0] = elem
                elif elem == Style.BLACKLETTER_FONT:
                    style[0] = elem

                elif elem in (Style.BOLD, Style.DIM):  # INTENSITY
                    style[1] = elem
                elif elem in (Style.OFF_BOLD, Style.OFF_DIM, Style.OFF_INTENSITY):
                    style[1] = None

                elif elem == Style.ITALIC:  # ITALIC
                    style[2] = elem
                elif elem == Style.OFF_ITALIC:
                    style[2] = None

                elif elem in (Style.UNDERLINE, Style.DOUBLY_UNDERLINE):  # UNDERLINE
                    style[3] = elem
                elif elem == Style.OFF_UNDERLINE:
                    style[3] = None

                elif elem in (Style.SLOW_BLINK, Style.RAPID_BLINK):  # BLINK
                    style[4] = elem
                elif elem == Style.OFF_BLINK:
                    style[4] = None

                elif elem == Style.INVERT:  # INVERT
                    style[5] = elem
                elif elem == Style.OFF_INVERT:
                    style[5] = None

                elif elem == Style.HIDE:  # HIDE
                    style[6] = elem
                elif elem == Style.OFF_HIDE:
                    style[6] = None

                elif elem == Style.STRIKE:  # STRIKE
                    style[7] = elem
                elif elem == Style.OFF_STRIKE:
                    style[7] = None

                elif elem == Style.OVERLINE:  # OVERLINE
                    style[8] = elem
                elif elem == Style.OFF_OVERLINE:
                    style[8] = None

                elif elem == Style.RESET:  # RESET
                    style = [None] * 11

                elif elem == Style.OFF_COLOR:  # OFF COLOR
                    style[9] = None
                elif elem == Style.OFF_BG_COLOR:
                    style[10] = None

                else:  # COLOR
                    if isinstance(elem, Color):
                        if elem.name.startswith('BG_'):
                            style[10] = elem
                        else:
                            style[9] = elem
                    else:
                        if elem.bg:
                            style[10] = elem
                        else:
                            style[9] = elem
            else:
                text_pool.append(elem)

        open_styles = []
        for given, parsed in zip(given_style, style):
            if parsed is None:
                if given is None:
                    continue
                open_styles.append(given.close())
            else:
                if given == parsed:
                    continue
                open_styles.append(parsed.open())
        open_style = ''.join(open_styles)

        result.append(open_style)

        for text in text_pool:
            if isinstance(text, str):
                result.append(text)
            elif isinstance(text, Iro):
                result.append(text.text)
            else:
                result.append(self.painter(text, style))

        for given, parsed in zip(given_style, style):
            if given is None:
                if parsed is None:
                    continue
                result.append(parsed.close())
            else:
                if given == parsed:
                    continue
                result.append(given.open())

        return ''.join(result)

    def open_styles(self, styles: List):
        result = []
        for style in styles:
            if style is None:
                continue
            if isinstance(style, ColorRGB) and self.disable_rgb:
                result.append(style.to_close_c256().open())
                continue
            result.append(style.open())
        return ''.join(result)

    def close_styles(self, styles: List):
        result = []
        for style in styles:
            if style is None:
                continue
            if isinstance(style, ColorRGB) and self.disable_rgb:
                result.append(style.to_close_c256().close())
                continue
            result.append(style.close())
        return ''.join(result)

    def __add__(self, other):
        if isinstance(other, str):
            return self.text + other
        elif isinstance(other, Iro):
            return Iro(self.text + other.text, disable_rgb=self.disable_rgb or other.disable_rgb)
        raise TypeError("Iro only can be added to `str` or `Iro`.")

    def __radd__(self, other):
        if isinstance(other, str):
            return other + self.text
        elif isinstance(other, Iro):
            return Iro(other.text + self.text, disable_rgb=self.disable_rgb or other.disable_rgb)
        raise TypeError("Iro only can be added to `str` or `Iro`.")

    def __str__(self):
        return self.text

    def __repr__(self):
        return 'Iro(text={}, disable_rgb={}, optimize_level={})'.format(repr(self.text),
                                                                        self.disable_rgb,
                                                                        self.optimize_level)


class Font(IroElement):
    def __init__(self, font_number: int):
        if not isinstance(font_number, int):
            try:
                font_number = int(font_number)
                warn('given `font_number` is not instance of int. given: {}. '
                     'Automatically converted to int...'.format(type(font_number)))
            except ValueError:
                warn('given `font_number` is not instance of int. Conversion failed.')
        if not 0 <= font_number <= 10:
            raise ValueError('`font_number` must be between 0 and 10. given: {}'.format(font_number))
        self.font_number = font_number

    def open(self):
        return '\033[{}m'.format(self.font_number + 11)

    def close(self):
        return '\033[10m'

    def __repr__(self):
        return 'Font(font_number={})'.format(self.font_number)


class Style(IroElement, Enum):
    RESET = 0
    BOLD = 1
    DIM = 2
    ITALIC = 3
    UNDERLINE = 4
    SLOW_BLINK = 5
    RAPID_BLINK = 6
    INVERT = 7
    HIDE = 8
    STRIKE = 9
    OVERLINE = 53

    BLACKLETTER_FONT = 20

    DOUBLY_UNDERLINE = 21

    OFF_INTENSITY = 22
    OFF_BOLD = 22
    OFF_DIM = 22
    OFF_ITALIC = 23
    OFF_UNDERLINE = 24
    OFF_BLINK = 25
    OFF_INVERT = 27
    OFF_HIDE = 28
    OFF_STRIKE = 29

    OFF_COLOR = 39
    OFF_BG_COLOR = 49

    OFF_OVERLINE = 55

    def open(self):
        return '\033[{}m'.format(self.value)

    def close(self):
        val = {1: 22, 2: 22, 3: 23, 4: 24, 5: 25, 6: 25, 7: 27, 8: 28, 9: 29, 20: 10, 21: 24}
        return '\033[{}m'.format(val.get(self.value, self.value))


class Color256(IroElement):
    color_map = {0: (0x00, 0x00, 0x00), 1: (0x80, 0x00, 0x00), 2: (0x00, 0x80, 0x00), 3: (0x80, 0x80, 0x00),
                 4: (0x00, 0x00, 0x80), 5: (0x80, 0x00, 0x80), 6: (0x00, 0x80, 0x80), 7: (0xc0, 0xc0, 0xc0),
                 8: (0x80, 0x80, 0x80), 9: (0xff, 0x00, 0x00), 10: (0x00, 0xff, 0x00), 11: (0xff, 0xff, 0x00),
                 12: (0x00, 0x00, 0xff), 13: (0xff, 0x00, 0xff), 14: (0x00, 0xff, 0xff), 15: (0xff, 0xff, 0xff),
                 16: (0x00, 0x00, 0x00), 17: (0x00, 0x00, 0x5f), 18: (0x00, 0x00, 0x87), 19: (0x00, 0x00, 0xaf),
                 20: (0x00, 0x00, 0xd7), 21: (0x00, 0x00, 0xff), 22: (0x00, 0x5f, 0x00), 23: (0x00, 0x5f, 0x5f),
                 24: (0x00, 0x5f, 0x87), 25: (0x00, 0x5f, 0xaf), 26: (0x00, 0x5f, 0xd7), 27: (0x00, 0x5f, 0xff),
                 28: (0x00, 0x87, 0x00), 29: (0x00, 0x87, 0x5f), 30: (0x00, 0x87, 0x87), 31: (0x00, 0x87, 0xaf),
                 32: (0x00, 0x87, 0xd7), 33: (0x00, 0x87, 0xff), 34: (0x00, 0xaf, 0x00), 35: (0x00, 0xaf, 0x5f),
                 36: (0x00, 0xaf, 0x87), 37: (0x00, 0xaf, 0xaf), 38: (0x00, 0xaf, 0xd7), 39: (0x00, 0xaf, 0xff),
                 40: (0x00, 0xd7, 0x00), 41: (0x00, 0xd7, 0x5f), 42: (0x00, 0xd7, 0x87), 43: (0x00, 0xd7, 0xaf),
                 44: (0x00, 0xd7, 0xd7), 45: (0x00, 0xd7, 0xff), 46: (0x00, 0xff, 0x00), 47: (0x00, 0xff, 0x5f),
                 48: (0x00, 0xff, 0x87), 49: (0x00, 0xff, 0xaf), 50: (0x00, 0xff, 0xd7), 51: (0x00, 0xff, 0xff),
                 52: (0x5f, 0x00, 0x00), 53: (0x5f, 0x00, 0x5f), 54: (0x5f, 0x00, 0x87), 55: (0x5f, 0x00, 0xaf),
                 56: (0x5f, 0x00, 0xd7), 57: (0x5f, 0x00, 0xff), 58: (0x5f, 0x5f, 0x00), 59: (0x5f, 0x5f, 0x5f),
                 60: (0x5f, 0x5f, 0x87), 61: (0x5f, 0x5f, 0xaf), 62: (0x5f, 0x5f, 0xd7), 63: (0x5f, 0x5f, 0xff),
                 64: (0x5f, 0x87, 0x00), 65: (0x5f, 0x87, 0x5f), 66: (0x5f, 0x87, 0x87), 67: (0x5f, 0x87, 0xaf),
                 68: (0x5f, 0x87, 0xd7), 69: (0x5f, 0x87, 0xff), 70: (0x5f, 0xaf, 0x00), 71: (0x5f, 0xaf, 0x5f),
                 72: (0x5f, 0xaf, 0x87), 73: (0x5f, 0xaf, 0xaf), 74: (0x5f, 0xaf, 0xd7), 75: (0x5f, 0xaf, 0xff),
                 76: (0x5f, 0xd7, 0x00), 77: (0x5f, 0xd7, 0x5f), 78: (0x5f, 0xd7, 0x87), 79: (0x5f, 0xd7, 0xaf),
                 80: (0x5f, 0xd7, 0xd7), 81: (0x5f, 0xd7, 0xff), 82: (0x5f, 0xff, 0x00), 83: (0x5f, 0xff, 0x5f),
                 84: (0x5f, 0xff, 0x87), 85: (0x5f, 0xff, 0xaf), 86: (0x5f, 0xff, 0xd7), 87: (0x5f, 0xff, 0xff),
                 88: (0x87, 0x00, 0x00), 89: (0x87, 0x00, 0x5f), 90: (0x87, 0x00, 0x87), 91: (0x87, 0x00, 0xaf),
                 92: (0x87, 0x00, 0xd7), 93: (0x87, 0x00, 0xff), 94: (0x87, 0x5f, 0x00), 95: (0x87, 0x5f, 0x5f),
                 96: (0x87, 0x5f, 0x87), 97: (0x87, 0x5f, 0xaf), 98: (0x87, 0x5f, 0xd7), 99: (0x87, 0x5f, 0xff),
                 100: (0x87, 0x87, 0x00), 101: (0x87, 0x87, 0x5f), 102: (0x87, 0x87, 0x87), 103: (0x87, 0x87, 0xaf),
                 104: (0x87, 0x87, 0xd7), 105: (0x87, 0x87, 0xff), 106: (0x87, 0xaf, 0x00), 107: (0x87, 0xaf, 0x5f),
                 108: (0x87, 0xaf, 0x87), 109: (0x87, 0xaf, 0xaf), 110: (0x87, 0xaf, 0xd7), 111: (0x87, 0xaf, 0xff),
                 112: (0x87, 0xd7, 0x00), 113: (0x87, 0xd7, 0x5f), 114: (0x87, 0xd7, 0x87), 115: (0x87, 0xd7, 0xaf),
                 116: (0x87, 0xd7, 0xd7), 117: (0x87, 0xd7, 0xff), 118: (0x87, 0xff, 0x00), 119: (0x87, 0xff, 0x5f),
                 120: (0x87, 0xff, 0x87), 121: (0x87, 0xff, 0xaf), 122: (0x87, 0xff, 0xd7), 123: (0x87, 0xff, 0xff),
                 124: (0xaf, 0x00, 0x00), 125: (0xaf, 0x00, 0x5f), 126: (0xaf, 0x00, 0x87), 127: (0xaf, 0x00, 0xaf),
                 128: (0xaf, 0x00, 0xd7), 129: (0xaf, 0x00, 0xff), 130: (0xaf, 0x5f, 0x00), 131: (0xaf, 0x5f, 0x5f),
                 132: (0xaf, 0x5f, 0x87), 133: (0xaf, 0x5f, 0xaf), 134: (0xaf, 0x5f, 0xd7), 135: (0xaf, 0x5f, 0xff),
                 136: (0xaf, 0x87, 0x00), 137: (0xaf, 0x87, 0x5f), 138: (0xaf, 0x87, 0x87), 139: (0xaf, 0x87, 0xaf),
                 140: (0xaf, 0x87, 0xd7), 141: (0xaf, 0x87, 0xff), 142: (0xaf, 0xaf, 0x00), 143: (0xaf, 0xaf, 0x5f),
                 144: (0xaf, 0xaf, 0x87), 145: (0xaf, 0xaf, 0xaf), 146: (0xaf, 0xaf, 0xd7), 147: (0xaf, 0xaf, 0xff),
                 148: (0xaf, 0xd7, 0x00), 149: (0xaf, 0xd7, 0x5f), 150: (0xaf, 0xd7, 0x87), 151: (0xaf, 0xd7, 0xaf),
                 152: (0xaf, 0xd7, 0xd7), 153: (0xaf, 0xd7, 0xff), 154: (0xaf, 0xff, 0x00), 155: (0xaf, 0xff, 0x5f),
                 156: (0xaf, 0xff, 0x87), 157: (0xaf, 0xff, 0xaf), 158: (0xaf, 0xff, 0xd7), 159: (0xaf, 0xff, 0xff),
                 160: (0xd7, 0x00, 0x00), 161: (0xd7, 0x00, 0x5f), 162: (0xd7, 0x00, 0x87), 163: (0xd7, 0x00, 0xaf),
                 164: (0xd7, 0x00, 0xd7), 165: (0xd7, 0x00, 0xff), 166: (0xd7, 0x5f, 0x00), 167: (0xd7, 0x5f, 0x5f),
                 168: (0xd7, 0x5f, 0x87), 169: (0xd7, 0x5f, 0xaf), 170: (0xd7, 0x5f, 0xd7), 171: (0xd7, 0x5f, 0xff),
                 172: (0xd7, 0x87, 0x00), 173: (0xd7, 0x87, 0x5f), 174: (0xd7, 0x87, 0x87), 175: (0xd7, 0x87, 0xaf),
                 176: (0xd7, 0x87, 0xd7), 177: (0xd7, 0x87, 0xff), 178: (0xd7, 0xaf, 0x00), 179: (0xd7, 0xaf, 0x5f),
                 180: (0xd7, 0xaf, 0x87), 181: (0xd7, 0xaf, 0xaf), 182: (0xd7, 0xaf, 0xd7), 183: (0xd7, 0xaf, 0xff),
                 184: (0xd7, 0xd7, 0x00), 185: (0xd7, 0xd7, 0x5f), 186: (0xd7, 0xd7, 0x87), 187: (0xd7, 0xd7, 0xaf),
                 188: (0xd7, 0xd7, 0xd7), 189: (0xd7, 0xd7, 0xff), 190: (0xd7, 0xff, 0x00), 191: (0xd7, 0xff, 0x5f),
                 192: (0xd7, 0xff, 0x87), 193: (0xd7, 0xff, 0xaf), 194: (0xd7, 0xff, 0xd7), 195: (0xd7, 0xff, 0xff),
                 196: (0xff, 0x00, 0x00), 197: (0xff, 0x00, 0x5f), 198: (0xff, 0x00, 0x87), 199: (0xff, 0x00, 0xaf),
                 200: (0xff, 0x00, 0xd7), 201: (0xff, 0x00, 0xff), 202: (0xff, 0x5f, 0x00), 203: (0xff, 0x5f, 0x5f),
                 204: (0xff, 0x5f, 0x87), 205: (0xff, 0x5f, 0xaf), 206: (0xff, 0x5f, 0xd7), 207: (0xff, 0x5f, 0xff),
                 208: (0xff, 0x87, 0x00), 209: (0xff, 0x87, 0x5f), 210: (0xff, 0x87, 0x87), 211: (0xff, 0x87, 0xaf),
                 212: (0xff, 0x87, 0xd7), 213: (0xff, 0x87, 0xff), 214: (0xff, 0xaf, 0x00), 215: (0xff, 0xaf, 0x5f),
                 216: (0xff, 0xaf, 0x87), 217: (0xff, 0xaf, 0xaf), 218: (0xff, 0xaf, 0xd7), 219: (0xff, 0xaf, 0xff),
                 220: (0xff, 0xd7, 0x00), 221: (0xff, 0xd7, 0x5f), 222: (0xff, 0xd7, 0x87), 223: (0xff, 0xd7, 0xaf),
                 224: (0xff, 0xd7, 0xd7), 225: (0xff, 0xd7, 0xff), 226: (0xff, 0xff, 0x00), 227: (0xff, 0xff, 0x5f),
                 228: (0xff, 0xff, 0x87), 229: (0xff, 0xff, 0xaf), 230: (0xff, 0xff, 0xd7), 231: (0xff, 0xff, 0xff),
                 232: (0x08, 0x08, 0x08), 233: (0x12, 0x12, 0x12), 234: (0x1c, 0x1c, 0x1c), 235: (0x26, 0x26, 0x26),
                 236: (0x30, 0x30, 0x30), 237: (0x3a, 0x3a, 0x3a), 238: (0x44, 0x44, 0x44), 239: (0x4e, 0x4e, 0x4e),
                 240: (0x58, 0x58, 0x58), 241: (0x62, 0x62, 0x62), 242: (0x6c, 0x6c, 0x6c), 243: (0x76, 0x76, 0x76),
                 244: (0x80, 0x80, 0x80), 245: (0x8a, 0x8a, 0x8a), 246: (0x94, 0x94, 0x94), 247: (0x9e, 0x9e, 0x9e),
                 248: (0xa8, 0xa8, 0xa8), 249: (0xb2, 0xb2, 0xb2), 250: (0xbc, 0xbc, 0xbc), 251: (0xc6, 0xc6, 0xc6),
                 252: (0xd0, 0xd0, 0xd0), 253: (0xda, 0xda, 0xda), 254: (0xe4, 0xe4, 0xe4), 255: (0xee, 0xee, 0xee)}

    def open(self):
        return '\033[{}8;5;{}m'.format(4 if self.bg else 3, self.color)

    def close(self):
        return '\033[{}9m'.format(4 if self.bg else 3)

    def __init__(self, color: int, bg=False):
        if not 0 <= color <= 255:
            raise ValueError("`color` must be between 0 and 255")
        self.color = color
        self.bg = bg

    def __repr__(self):
        return 'Color256(color={}, value="#{:02x}{:02x}{:02x}", bg={})'.format(self.color,
                                                                               self.color_map[self.color][0],
                                                                               self.color_map[self.color][1],
                                                                               self.color_map[self.color][2],
                                                                               self.bg)


class ColorRGB(IroElement):
    def __init__(self, r: int, g: int, b: int, bg: bool = False):
        self.r = round(r)
        self.g = round(g)
        self.b = round(b)
        self.bg = bg
        if not 0 <= self.r <= 255 or not 0 <= self.g <= 255 or not 0 <= self.b <= 255:
            raise ValueError('Given number is invalid. must be between 0 and 255')

    @classmethod
    def from_color_code(cls, color_code: str, bg: bool = False):
        color_code = color_code.lstrip('#')
        if len(color_code) != 6:
            raise ValueError("length of `color_code` must be 6.")
        r, g, b = int(color_code[:2], 16), int(color_code[2:4], 16), int(color_code[4:], 16)
        return ColorRGB(r, g, b, bg)

    def to_close_c256(self) -> Color256:
        min_diff = float('inf')
        color = None
        for i, v in Color256.color_map.items():
            diff = math.sqrt(2 * (v[0] - self.r) ** 2 + 4 * (v[1] - self.g) ** 2 + 3 * (v[2] - self.b) ** 2)
            if diff < min_diff:
                min_diff = diff
                color = i
        return Color256(color, self.bg)

    def open(self):
        return '\033[{}8;2;{};{};{}m'.format(4 if self.bg else 3, self.r, self.g, self.b)

    def close(self):
        return '\033[{}9m'.format(4 if self.bg else 3)

    def __repr__(self):
        return 'ColorRGB(r={}, g={}, b={}, bg={})'.format(self.r, self.g, self.b, self.bg)


class Color(IroElement, Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97

    BG_BLACK = 40
    BG_RED = 41
    BG_GREEN = 42
    BG_YELLOW = 43
    BG_BLUE = 44
    BG_MAGENTA = 45
    BG_CYAN = 46
    BG_WHITE = 47

    BG_BRIGHT_BLACK = 100
    BG_BRIGHT_RED = 101
    BG_BRIGHT_GREEN = 102
    BG_BRIGHT_YELLOW = 103
    BG_BRIGHT_BLUE = 104
    BG_BRIGHT_MAGENTA = 105
    BG_BRIGHT_CYAN = 106
    BG_BRIGHT_WHITE = 107

    def open(self):
        return '\033[{}m'.format(self.value)

    def close(self):
        if self.name.startswith('BG_'):
            return '\033[49m'
        return '\033[39m'
