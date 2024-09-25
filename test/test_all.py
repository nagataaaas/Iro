from src.iro import Iro, Color256, ColorRGB, Style, FGColor, BGColor, Font


class Test:
    class TestIro:
        class TestOnlyString:
            def test_no_sep(self):
                result = str(Iro("normal ", "normal"))
                print(result)
                assert result == f"normal normal{Style.RESET.open}"

            def test_str_sep(self):
                result = str(Iro("normal", "normal", "!", sep=" "))
                print(result)
                assert result == f"normal normal !{Style.RESET.open}"

        class TestNestedIro:
            def test_list_sep(self):
                result = str(Iro("normal", Iro("n", "rmal", sep="o"), "!", sep=" "))
                print(result)
                assert result == f"normal normal !{Style.RESET.open}"

            def test_list_sep_out_of_index(self):
                result = str(Iro("normal", Iro("n", Iro("r", "mal"), sep="o"), "!", sep=" "))
                print(result)
                assert result == f"normal normal !{Style.RESET.open}"

        class TestStyle:
            def test_style(self):
                result = str(Iro("bold", Style.BOLD, "bold", "!", sep=" "))
                print(result)
                assert result == f"{Style.BOLD.open}bold bold !{Style.RESET.open}"

            def test_style_no_collect_first(self):
                result = str(Iro("normal", Style.BOLD, "bold", "!", sep=" ", collect_styles_first=False))
                print(result)
                assert result == f"normal{Style.BOLD.open} bold !{Style.RESET.open}"

            def test_style_multiple_no_same_category(self):
                result = str(Iro("bold-red", Style.BOLD, FGColor.BRIGHT_RED, "bold-red", "!", sep=" "))
                print(result)
                assert result == f"{Style.BOLD.open}{FGColor.BRIGHT_RED.open}bold-red bold-red !{Style.RESET.open}"

            def test_style_multiple_same_category(self):
                result = str(Iro("bold-dim", Style.BOLD, Style.DIM, "bold-dim", "!", sep=" "))
                print(result)
                assert result == f"{Style.BOLD.open}{Style.DIM.open}bold-dim bold-dim !{Style.RESET.open}"

            def test_style_multiple_same_category_no_collect_styles_first(self):
                result = str(
                    Iro("normal", Style.BOLD, "bold", Style.DIM, "bold-dim", Style.OFF_BOLD, "dim", "!", sep=" ",
                        collect_styles_first=False))
                print(result)
                assert result == f"normal{Style.BOLD.open} bold{Style.DIM.open} bold-dim{Style.BOLD.close}{Style.DIM.open} dim !{Style.RESET.open}"

            def test_style_multiple_same_category_collect(self):
                result = str(Iro("bold-dim", Style.BOLD, "bold-dim", Style.DIM, "bold-dim", "!", sep=" "))
                print(result)
                assert result == f"{Style.BOLD.open}{Style.DIM.open}bold-dim bold-dim bold-dim !{Style.RESET.open}"

            def test_style_test_font_collect(self):
                result = str(
                    Iro(FGColor.RED, "font-1", Font(1), [Font(2), "font-2", [Style.OFF_FONT, "default"], "font-2"],
                        "font-1", sep=" "))
                print(result)
                assert result == f"{FGColor.RED.open}{Font(1).open}font-1 {Font(2).open}font-2 {Font(0).open}default{Font(2).open} font-2{Font(1).open} font-1{Style.RESET.open}"

            def test_style_test_font_no_collect(self):
                result = str(
                    Iro(FGColor.RED, "font-1", Font(1), [Font(2), "font-2", [Style.OFF_FONT, "default"], "font-2"],
                        "font-1", sep=" ", collect_styles_first=False))
                print(result)
                assert result == f"{FGColor.RED.open}font-1{Font(1).open} {Font(2).open}font-2 {Font(0).open}default{Font(2).open} font-2{Font(1).open} font-1{Style.RESET.open}"

            def test_style_test_sep_only_between_value(self):
                result = str(
                    Iro(FGColor.RED, "a", FGColor.BLUE, Font(1), ["c", FGColor.RED, "d", BGColor.BLUE, ], "e", sep="_"))
                print(result)
                assert result == f"{FGColor.BLUE.open}{Font(1).open}a_{FGColor.RED.open}{BGColor.BLUE.open}c_d{FGColor.BLUE.open}{BGColor.BLUE.close}_e{Style.RESET.open}"

            def test_style_test_sep_only_between_value_no_correct(self):
                result = str(
                    Iro(FGColor.RED, "font-1", Font(1), [Font(2), "font-2", [Style.OFF_FONT, "default"], "font-2"],
                        "font-1", sep=" ", collect_styles_first=False))
                print(result)
                assert result == f"{FGColor.RED.open}font-1{Font(1).open} {Font(2).open}font-2 {Font(0).open}default{Font(2).open} font-2{Font(1).open} font-1{Style.RESET.open}"

        class TestNestedStyles:
            def test_style_nested(self):
                result = str(Iro(Style.UNDERLINE, "under", [Style.BOLD, "under-bold"], "under", "!", sep=" "))
                print(result)
                assert result == f"{Style.UNDERLINE.open}under {Style.BOLD.open}under-bold{Style.BOLD.close} under !{Style.RESET.open}"

            def test_style_nested_only_inside(self):
                result = str(Iro("normal", [Style.BOLD, "bold"], "normal", "!", sep=" "))
                print(result)
                assert result == f"normal {Style.BOLD.open}bold{Style.RESET.open} normal !{Style.RESET.open}"

            def test_style_nested_same_style(self):
                result = str(Iro(Style.BOLD, "bold", [Style.BOLD, "bold"], "bold", "!", sep=" "))
                print(result)
                assert result == f"{Style.BOLD.open}bold bold bold !{Style.RESET.open}"

            def test_style_nested_same_category(self):
                result = str(Iro(Style.BOLD, "bold", [Style.DIM, "bold-dim"], "bold", "!", sep=" "))
                print(result)
                assert result == f"{Style.BOLD.open}bold {Style.DIM.open}bold-dim{Style.DIM.close}{Style.BOLD.open} bold !{Style.RESET.open}"

            def test_style_nested_fg_color(self):
                result = str(Iro(FGColor.RED, "red", [FGColor.BLUE, "blue"], "red", "!", sep=" "))
                print(result)
                assert result == f"{FGColor.RED.open}red {FGColor.BLUE.open}blue{FGColor.RED.open} red !{Style.RESET.open}"

            def test_style_nested_color(self):
                result = str(Iro(FGColor.RED, "red", [FGColor.BLUE, "blue"], "red", "!", sep=" "))
                print(result)
                assert result == (f"{FGColor.RED.open}red "
                                  f"{FGColor.BLUE.open}blue"
                                  f"{FGColor.RED.open} red !"
                                  f"{Style.RESET.open}")

            def test_style_nested_various_colors(self):
                result = str(
                    Iro(FGColor.RED, "red", [Color256(12), "blue", [ColorRGB(0, 0xff, 0), "green", ], "blue"], "red"))
                print(result)
                assert result == (f"{FGColor.RED.open}red"
                                  f"{Color256(12).open}blue"
                                  f"{ColorRGB(0, 0xff, 0).open}green"
                                  f"{Color256(12).open}blue"
                                  f"{FGColor.RED.open}red"
                                  f"{Style.RESET.open}")

            def test_style_nested_various_bg_colors(self):
                result = str(
                    Iro(BGColor.RED, "red",
                        [Color256(12, bg=True), "blue", [ColorRGB(0, 0xff, 0, bg=True), "green", ], "blue"], "red"))
                print(result)
                assert result == (f"{BGColor.RED.open}red"
                                  f"{Color256(12, bg=True).open}blue"
                                  f"{ColorRGB(0, 0xff, 0, bg=True).open}green"
                                  f"{Color256(12, bg=True).open}blue"
                                  f"{BGColor.RED.open}red"
                                  f"{Style.RESET.open}")

            def test_style_nested_loop(self):
                result = str(
                    Iro(Style.BOLD, "bold", [
                        Style.OFF_BOLD, Style.DIM, "dim", [
                            Style.OFF_DIM, Style.BOLD, "bold", [
                                Style.OFF_BOLD, Style.DIM, "dim"
                            ], "bold"
                        ], "dim"
                    ],
                        "bold", sep=" "))
                print(result)
                assert result == (f"{Style.BOLD.open}bold "
                                  f"{Style.BOLD.close}{Style.DIM.open}dim "
                                  f"{Style.DIM.close}{Style.BOLD.open}bold "
                                  f"{Style.BOLD.close}{Style.DIM.open}dim"
                                  f"{Style.DIM.close}{Style.BOLD.open} bold"
                                  f"{Style.BOLD.close}{Style.DIM.open} dim"
                                  f"{Style.DIM.close}{Style.BOLD.open} bold"
                                  f"{Style.RESET.open}")

            def test_nested_reset(self):
                result = str(
                    Iro(Style.BOLD, "bold", [
                        Style.DIM, "bold-dim", [
                            Style.RESET, "normal", [
                                Style.DIM, "dim"
                            ], "normal"
                        ], "bold-dim"
                    ],
                        "bold", sep=" "))
                print(result)
                assert result == (f"{Style.BOLD.open}bold "
                                  f"{Style.DIM.open}bold-dim "
                                  f"{Style.RESET.open}normal "
                                  f"{Style.DIM.open}dim"
                                  f"{Style.RESET.open} normal"
                                  f"{Style.BOLD.open}{Style.DIM.open} bold-dim"
                                  f"{Style.DIM.close}{Style.BOLD.open} bold"
                                  f"{Style.RESET.open}")

    class TestStyle:
        def test_normal_reset_integrity(self):
            assert Style.RESET is Style.NORMAL
