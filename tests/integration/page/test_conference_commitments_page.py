from soccer_sdk_utils.gender import Gender
from soccer_sdk_utils.division import Division

from topdrawersoccer_sdk.page.conference import ConferenceCommitmentsPage


def test_get_commitments_wcc_2022():
    # Arrange
    page = ConferenceCommitmentsPage(Gender.Female, Division.DI, "West Coast")

    # Act
    commitments = page.get_commitments("2022")

    # Assert
    assert commitments is not None
    assert len(commitments) == 63
