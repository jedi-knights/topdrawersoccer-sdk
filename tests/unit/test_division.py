from topdrawersoccer_sdk.division import Division, string_to_division


def test_division_str():
    division = Division.DI
    assert str(division) == "di"


class TestStringToDivision:
    def test_none(self):
        assert string_to_division(None) is None

    def test_empty(self):
        assert string_to_division("") is None

    def test_spaces(self):
        assert string_to_division("    ") is None

    def test_all_lower_case(self):
        assert string_to_division("all") == Division.All

    def test_all_upper_case(self):
        assert string_to_division("ALL") == Division.All

    def test_all_mixed_case(self):
        assert string_to_division("All") == Division.All
