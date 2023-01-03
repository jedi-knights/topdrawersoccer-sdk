import pytest

from soccer_sdk_utils.division import Division
from topdrawersoccer_sdk.conference import division_to_conference_url


class TestDivisionToConferenceUrl:
    def test_all(self):
        # Arrange
        division = Division.All

        # Act
        with pytest.raises(ValueError, match="Unsupported division 'all'"):
            division_to_conference_url(division)

    def test_di(self):
        # Arrange
        division = Division.DI
        expected = "https://www.topdrawersoccer.com/college-soccer/college-conferences/di/divisionid-1"

        # Act
        actual = division_to_conference_url(division)

        # Assert
        assert actual == expected

    def test_dii(self):
        # Arrange
        division = Division.DII
        expected = "https://www.topdrawersoccer.com/college-soccer/college-conferences/dii/divisionid-2"

        # Act
        actual = division_to_conference_url(division)

        # Assert
        assert actual == expected

    def test_diii(self):
        # Arrange
        division = Division.DIII
        expected = "https://www.topdrawersoccer.com/college-soccer/college-conferences/diii/divisionid-3"

        # Act
        actual = division_to_conference_url(division)

        # Assert
        assert actual == expected

    def test_naia(self):
        # Arrange
        division = Division.NAIA
        expected = "https://www.topdrawersoccer.com/college-soccer/college-conferences/naia/divisionid-4"

        # Act
        actual = division_to_conference_url(division)

        # Assert
        assert actual == expected

    def test_njcaa(self):
        # Arrange
        division = Division.NJCAA
        expected = "https://www.topdrawersoccer.com/college-soccer/college-conferences/njcaa/divisionid-5"

        # Act
        actual = division_to_conference_url(division)

        # Assert
        assert actual == expected
