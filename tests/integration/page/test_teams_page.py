import pytest

from soccer_sdk_utils.division import Division
from soccer_sdk_utils.gender import Gender

from topdrawersoccer_sdk.page.team import TeamsPage, get_division_by_conference_name


@pytest.fixture
def di_teams_page():
    return TeamsPage(Division.DI)


def test_get_conferences(di_teams_page):
    # Act
    conferences = di_teams_page.get_conferences()

    # Assert
    assert conferences is not None
    assert len(conferences) == 32


def test_get_conference_by_name(di_teams_page):
    # Arrange
    conference_name = "Big Ten"

    # Act
    conference = di_teams_page.get_conference_by_name(conference_name)

    # Assert
    assert conference is not None
    assert conference.name == conference_name
    assert conference.division == Division.DI
    assert conference.urls.tds.endswith("?genderId=&conferenceId=7&conferenceName=big-ten")
    assert conference.ids.tds == "7"


def test_get_conference_by_name_not_found(di_teams_page):
    # Act
    conference = di_teams_page.get_conference_by_name("not found")

    # Assert
    assert conference is None


def test_get_schools_by_conference_female_wcc(di_teams_page):
    # Arrange
    conference_name = "West Coast"

    # Act
    schools = di_teams_page.get_schools_by_conference_name(conference_name, Gender.Female)

    # Assert
    assert schools is not None
    assert len(schools) == 10


def test_get_schools_by_conference_male_wcc(di_teams_page):
    # Arrange
    conference_name = "West Coast"

    # Act
    schools = di_teams_page.get_schools_by_conference_name(conference_name, Gender.Male)

    # Assert
    assert schools is not None
    assert len(schools) == 8


def test_get_conference_names(di_teams_page):
    # Act
    names = di_teams_page.get_conference_names()

    # Assert
    assert names == ['ASUN',
                     'America East',
                     'American Athletic',
                     'Atlantic 10',
                     'Atlantic Coast',
                     'Big 12',
                     'Big East',
                     'Big Sky',
                     'Big South',
                     'Big Ten',
                     'Big West',
                     'Colonial Athletic Association',
                     'Conference USA',
                     'Horizon League',
                     'Independent',
                     'Ivy League',
                     'Metro Atlantic Athletic Conference',
                     'Mid-American',
                     'Missouri Valley',
                     'Mountain West',
                     'Northeast',
                     'Ohio Valley',
                     'Pacific 12',
                     'Patriot League',
                     'SEC',
                     'Southern',
                     'Southland',
                     'Southwestern Athletic',
                     'Summit League',
                     'Sun Belt',
                     'West Coast',
                     'Western Athletic']


class TestGetClgIdByName:
    def test_santa_clara_men(self, di_teams_page):
        # Arrange
        school_name = "Santa Clara"
        gender = Gender.Male

        # Act
        school_id = di_teams_page.get_clgid_by_name(school_name, gender)

        # Assert
        assert school_id == "187"

    def test_santa_clara_women(self, di_teams_page):
        # Arrange
        school_name = "Santa Clara"
        gender = Gender.Female

        # Act
        school_id = di_teams_page.get_clgid_by_name(school_name, gender)

        # Assert
        assert school_id == "474"

    def test_stanford_women(self, di_teams_page):
        # Arrange
        school_name = "Stanford"
        gender = Gender.Female

        # Act
        school_id = di_teams_page.get_clgid_by_name(school_name, gender)

        # Assert
        assert school_id == "267"

    def test_byu_men(self, di_teams_page):
        # Arrange
        school_name = "BYU"
        gender = Gender.Male

        # Act
        school_id = di_teams_page.get_clgid_by_name(school_name, gender)

        # Assert
        assert school_id is None

    def test_byu_women(self, di_teams_page):
        # Arrange
        school_name = "BYU"
        gender = Gender.Female

        # Act
        school_id = di_teams_page.get_clgid_by_name(school_name, gender)

        # Assert
        assert school_id == "251"


def test_get_division_by_conference_name_wcc():
    # Arrange
    conference_name = "West Coast"

    # Act
    division = get_division_by_conference_name(conference_name)

    # Assert
    assert division == Division.DI
