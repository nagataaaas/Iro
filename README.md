IRO
===

Easy and powerful Colorizer for Python!

Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/nagataaaas/Iro)

The depth represents a block and affects all elements within that block.

```python
from iro import Iro, Color, Style, ColorRGB, Color256

from colorsys import hls_to_rgb

success = Iro((Color.GREEN, "[  SUCCESS ]"))
error = Iro((Color.WHITE, Style.DOUBLY_UNDERLINE, ColorRGB(255, 0, 0, bg=True), "[   ERROR  ]"), disable_rgb=False)
warning = Iro((Color.YELLOW, Color256(255, bg=True), "[  WARNING ]"))
deprecated = Iro((Color256(7), Color256(239, True), Style.STRIKE, "[DEPRECATED]"))

print(success, 'code success.')
print(error, 'code failed!!')
print(warning, 'maybe something wrong.')
print(deprecated, 'this function is deprecated.')

print(Iro([
    Color.RED, "Off course, You can nest styles. ", 
    [
        Style.ITALIC,
        "This is RED and ITALIC. "
    ], 
    [
        Color.BLUE,
        Color.BG_BRIGHT_YELLOW,
        Style.UNDERLINE,
        "This is BLUE, BG_YELLOW and UNDERLINED."
    ],
    " Finally back to only RED!"
]))

for h in range(256):
    print(Iro([ColorRGB(*map(lambda x: x * 255, hls_to_rgb(h / 256, 0.7, 1)), bg=True), ' '], disable_rgb=False), end='')
```
**output**
![output](https://github.com/nagataaaas/Iro/blob/main/assets/capture1.png?raw=true)

# Installation
    
    $ pip install iro

# Document
## `Iro(text: Iterable, disable_rgb: bool = True)`
- text: Iterable of `str`, `Style`, `Color`, `Color256`, `ColorRGB`, `Font` and `Iro`.
- disable_rgb: if `True`, `ColorRGB` will be converted to similar color of `Color256`. `ColorRGB` is not supported in some Terminals.

## Style
Enum of defined `Styling`.

    BOLD 
    DIM 
    ITALIC 
    UNDERLINE 
    SLOW_BLINK 
    RAPID_BLINK 
    INVERT 
    HIDE 
    STRIKE 
    BLACKLETTER_FONT 
    DOUBLY_UNDERLINE 
    
## Color
Enum of 3-bit and 4-bit color.

    BLACK 
    RED 
    GREEN 
    YELLOW 
    BLUE 
    MAGENTA 
    CYAN 
    WHITE 

    BRIGHT_BLACK 
    BRIGHT_RED 
    BRIGHT_GREEN 
    BRIGHT_YELLOW 
    BRIGHT_BLUE 
    BRIGHT_MAGENTA 
    BRIGHT_CYAN 
    BRIGHT_WHITE 

    BG_BLACK 
    BG_RED 
    BG_GREEN 
    BG_YELLOW 
    BG_BLUE 
    BG_MAGENTA 
    BG_CYAN 
    BG_WHITE 

    BG_BRIGHT_BLACK 
    BG_BRIGHT_RED 
    BG_BRIGHT_GREEN 
    BG_BRIGHT_YELLOW 
    BG_BRIGHT_BLUE 
    BG_BRIGHT_MAGENTA 
    BG_BRIGHT_CYAN 
    BG_BRIGHT_WHITE 

These Colors are supported in almost all of terminals.

In terms of portability, this is how most coloring should be done.

## Color256(number: int, bg: bool = False)
- number: number of pre-defined 8-bit color. `0 <= number <= 255`
- bg: if `True`, This color will be applied to background.

## ColorRGB(r: int, g: int, b: int, bg: bool = False)
- r, g, b: value of RGB. if `float` is given, number will be `round`ed. `0 <= number <= 255`
- bg: if `True`, This color will be applied to background.

### ColorRGB.from_color_code(color_code: str, bg: bool = False)
- color_code: `str` that matches to regex `#?[0-9a-fA-F]{6}`
- bg: if `True`, This color will be applied to background.

## Font(font_number: int)
- font_number: number of font. `0` is default font. up to `10`.

# Q&A
### My `ColorRGB` and `Color256` is not working!
> The problem is most likely caused by the console not supporting it. Please check.

### My `ColorRGB` is not the color that I specified!
> If `disable_rgb` is `True`, `Iro` will convert every `ColorRGB` to similar `Color256`. Make sure `disable_rgb` is set to `False`.

### Coloring, Styling and Fonts are not working!
> Not all features are supported in every console. Try another one.

### Weird string like `[0m[0m[5m[48;2;168;102;255m [0m[0m[5m` are showing up and not working at all!
> Your console is not supporting ANSI escape sequences. Try another console. Or, you can try `colorama`.\
> insert this code below in your Script
>
    from colorama import init
    init()