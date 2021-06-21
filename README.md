IRO
===

Easy and powerful Colorizer for Python!

Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/nagataaaas/Iro)

```python
from iro import Iro, Color, Style, RGBColor, Color256

from colorsys import hls_to_rgb

success = Iro((Color.GREEN, "[  SUCCESS ]"))
error = Iro((Color.WHITE, Style.DOUBLY_UNDERLINE, RGBColor(255, 0, 0, bg=True), "[   ERROR  ]"), disable_rgb=False)
warning = Iro((Color.YELLOW, Color256(255, bg=True), "[  WARNING ]"))
deprecated = Iro((Color256(7), Color256(239, True), Style.STRIKE, "[DEPRECATED]"))

print(success, 'code success.')
print(error, 'code failed!!')
print(warning, 'maybe something wrong.')
print(deprecated, 'this function is deprecated.')

print(Iro([
    Color.RED, "Off course, You can nest styles. ", [
        Style.ITALIC,
        "This is RED and ITALIC. "
    ], [
        Color.BLUE,
        Color.BG_BRIGHT_YELLOW,
        Style.UNDERLINE,
        "This is BLUE, BG_YELLOW and UNDERLINED."
    ],
    " Finally back to only RED!"
]))

for h in range(256):
    print(Iro([RGBColor(*map(lambda x: x * 255, hls_to_rgb(h / 256, 0.7, 1)), bg=True), ' '], disable_rgb=False), end='')
```
