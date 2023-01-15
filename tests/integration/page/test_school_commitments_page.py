from soccer_sdk_utils.gender import Gender

from topdrawersoccer_sdk.page.conference import SchoolCommitmentsPage


class TestGetCommitments:
    def test_female_santa_clara_2023(self):
        # Arrange
        gender = Gender.Female
        school = "Santa Clara"
        year = "2023"
        page = SchoolCommitmentsPage(gender, school)

        # Act
        commitments = page.get_commitments(year)

        # Assert
        assert commitments is not None
        assert len(commitments) == 6
