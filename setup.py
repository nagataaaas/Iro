"""
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
    print(Iro([RGBColor(*map(lambda x: x * 255, hls_to_rgb(h / 256, 0.7, 1)), bg=True), ' '], disable_rgb=False), end='')
```
"""

from setuptools import setup
from os import path

about = {}
with open("iro/__about__.py") as f:
    exec(f.read(), about)

here = path.abspath(path.dirname(__file__))

setup(name=about["__title__"],
      version=about["__version__"],
      url=about["__url__"],
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      description=about["__description__"],
      long_description=__doc__,
      long_description_content_type="text/markdown",
      install_requires=[],
      packages=["iro"],
      zip_safe=True,
      platforms="any",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Environment :: Console"
      ])
