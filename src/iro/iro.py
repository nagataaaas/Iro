from typing import Iterable, List, Literal, Any, Union

from .styles import IroElement, ColorRGB, Style, StyleState


class Iro:
    def __init__(self, *values: Any, disable_rgb: bool = True,
                 sep: Union[str, "Iro"] = "", collect_styles_first: bool = True):
        """

        :param values: texts to colorize
        :param disable_rgb: whether to disable RGB color or not
        :param sep: separator between texts. if isinstance of str, it will be used as separator. if isinstance of Iterable[str], it will be used as separator for each depth.
        :param collect_first: whether to collect styles at first or not
        """

        self.disable_rgb: bool = disable_rgb
        self.sep = sep
        self.collect_styles_first = collect_styles_first
        self.values = list(values)

    def paint(self, given_style=None, depth: int = 0) -> str:
        """
        Paint texts with given styles.
        :param given_style: given styles
        :param depth: depth of recursion
        :return: painted text
        """
        result, _ = self._paint(self.values, given_style, depth)
        return result

    def _paint(self, values: Iterable, given_style: Union[StyleState, None] = None, depth: int = 0) -> (
            str, StyleState):
        current_style = given_style.copy() if given_style else StyleState()

        result: List = []

        if self.collect_styles_first:
            for item in values:
                if isinstance(item, IroElement):
                    current_style = current_style.copy_with(item)

            result.append((given_style or StyleState()).diff_sequence(current_style))

        found_visible = False
        last_child_style_state: Union[StyleState, None] = None

        for i, item in enumerate(values):
            if depth == 0 and i == 0 and item is Style.RESET:
                result.append(Style.RESET.open)

            if isinstance(item, IroElement):
                if not self.collect_styles_first:
                    next_style = current_style.copy_with(item)
                    result.append(current_style.diff_sequence(next_style))
                    current_style = next_style
                continue

            if last_child_style_state:
                result.append(last_child_style_state.diff_sequence(current_style))
                last_child_style_state = None

            if found_visible and self.sep:
                if isinstance(self.sep, Iro):
                    child_paint_result, _last_child_style_state = self._paint_child(self.sep, current_style, depth)
                    result.append(child_paint_result)
                    result.append(_last_child_style_state.diff_sequence(current_style))
                else:
                    result.append(self.sep)

            if isinstance(item, str):
                result.append(item)
            else:
                child_paint_result, last_child_style_state = self._paint_child(item, current_style, depth)
                result.append(child_paint_result)
            found_visible = True

        if depth == 0:
            result.append(Style.RESET.open)

        return ''.join(result), last_child_style_state or current_style

    def _paint_child(self, value: Any, current_style: StyleState, current_depth: int) -> (str, StyleState):
        if isinstance(value, Iro):
            return value._paint(value.values, current_style, current_depth + 1)
        return self._paint(value, current_style, current_depth + 1)

    @staticmethod
    def open_styles(styles: Iterable[IroElement], disable_rgb: bool):
        result = []
        for style in styles:
            if not disable_rgb and isinstance(style, ColorRGB):
                result.append(style.to_close_c256().open)
                continue
            result.append(style.open)
        return ''.join(result)

    @staticmethod
    def close_styles(styles: List[IroElement], disable_rgb: bool):
        result = []
        for style in styles:
            if not disable_rgb and isinstance(style, ColorRGB):
                result.append(style.to_close_c256().close)
                continue
            result.append(style.close)
        return ''.join(result)

    def __add__(self, other):
        if isinstance(other, str):
            return self.values + [other]
        elif isinstance(other, Iro):
            return Iro(self.values + other.values, disable_rgb=self.disable_rgb or other.disable_rgb)
        raise TypeError("Iro only can be added to `str` or `Iro`.")

    def __radd__(self, other):
        if isinstance(other, str):
            return [other] + self.values
        elif isinstance(other, Iro):
            return Iro(other.values + self.values, disable_rgb=self.disable_rgb or other.disable_rgb)
        raise TypeError("Iro only can be added to `str` or `Iro`.")

    @property
    def text(self) -> str:
        return self.str

    @property
    def str(self) -> str:
        return str(self)

    def __str__(self):
        return self.paint()

    def __repr__(self):
        return ('Iro(values={}, disable_rgb={}, sep={}, collect_styles_first={})').format(repr(self.values),
                                                                                          self.disable_rgb,
                                                                                          repr(self.sep),
                                                                                          self.collect_styles_first)
