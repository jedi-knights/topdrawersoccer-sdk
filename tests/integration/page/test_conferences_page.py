import pytest
from soccer_sdk_utils.gender import Gender

from topdrawersoccer_sdk.page import conference

from topdrawersoccer_sdk.page.conference import ConferencesPage


@pytest.fixture
def di_conferences_page():
    return ConferencesPage(division=conference.Division.DI)


class TestGetConferenceByName:
    def test_none(self, di_conferences_page):
        assert di_conferences_page.get_conference_by_name(None, Gender.Female) is None

    def test_empty(self, di_conferences_page):
        assert di_conferences_page.get_conference_by_name("", Gender.Female) is None

    def test_spaces(self, di_conferences_page):
        assert di_conferences_page.get_conference_by_name("    ", Gender.Female) is None

    def test_all_lower_case(self, di_conferences_page):
        assert di_conferences_page.get_conference_by_name("atlantic coast", Gender.Female) is not None

    def test_all_upper_case(self, di_conferences_page):
        assert di_conferences_page.get_conference_by_name("Atlantic Coast", Gender.Female) is not None

    def test_all_mixed_case(self, di_conferences_page):
        assert di_conferences_page.get_conference_by_name("Atlantic coast", Gender.Female) is not None

    def test_not_found(self, di_conferences_page):
        assert di_conferences_page.get_conference_by_name("not found", Gender.Female) is None

    def test_found(self, di_conferences_page):
        conference = di_conferences_page.get_conference_by_name("Atlantic Coast", Gender.Female)

        assert conference is not None
        assert conference.name == "Atlantic Coast"
        assert conference.gender == Gender.Female
        assert conference.urls.tds.endswith("/atlantic-coast/cfid-3")
        assert conference.ids.tds == "3"
        assert conference.slug == "atlantic-coast"


class TestHasConference:
    def test_sec(self, di_conferences_page):
        assert di_conferences_page.has_conference("SEC", Gender.Female)

    def test_atlantic_coast(self, di_conferences_page):
        assert di_conferences_page.has_conference("Atlantic Coast", Gender.Female)

    def test_atlantic_coast_lowercase(self, di_conferences_page):
        assert di_conferences_page.has_conference("atlantic coast", Gender.Female)

    def test_missing(self, di_conferences_page):
        assert not di_conferences_page.has_conference("missing", Gender.Female)


class TestGetDivisionByConferenceName:
    def test_di_sec(self):
        # Arrange
        name = "SEC"
        gender = Gender.Female

        # Act
        division = ConferencesPage.get_division_by_conference_name(name, gender)

        # Assert
        assert division == conference.Division.DI

    def test_dii_heartland(self):
        # Arrange
        name = "Heartland"
        gender = Gender.Female

        # Act
        division = ConferencesPage.get_division_by_conference_name(name, gender)

        # Assert
        assert division == conference.Division.DII

    def test_diii_freedom(self):
        # Arrange
        name = "Freedom"
        gender = Gender.Female

        # Act
        division = ConferencesPage.get_division_by_conference_name(name, gender)

        # Assert
        assert division == conference.Division.DIII

    def test_naia_frontier(self):
        # Arrange
        name = "Frontier"
        gender = Gender.Female

        # Act
        division = ConferencesPage.get_division_by_conference_name(name, gender)

        # Assert
        assert division == conference.Division.NAIA

    def test_njcaa_foothill(self):
        # Arrange
        name = "Foothill"
        gender = Gender.Female

        # Act
        division = ConferencesPage.get_division_by_conference_name(name, gender)

        # Assert
        assert division == conference.Division.NJCAA


class TestGetConferenceNames:
    def test_womens_di(self, di_conferences_page):
        # Arrange
        gender = Gender.Female

        # Act
        names = di_conferences_page.get_conference_names(gender)

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

    def test_mens_di(self, di_conferences_page):
        # Arrange
        gender = Gender.Male

        # Act
        names = di_conferences_page.get_conference_names(gender)

        # Assert
        assert names == ['ASUN',
                         'America East',
                         'American Athletic',
                         'Atlantic 10',
                         'Atlantic Coast',
                         'Big East',
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
                         'Northeast',
                         'Ohio Valley',
                         'Pacific 12',
                         'Patriot League',
                         'Southern',
                         'Summit League',
                         'Sun Belt',
                         'West Coast',
                         'Western Athletic']


class TestGetConferenceById:
    def test_sec(self, di_conferences_page):
        # Arrange
        target_id = "1044"
        gender = Gender.Female

        # Act
        conference = di_conferences_page.get_conference_by_id(target_id, gender)

        # Assert
        assert conference is not None
        assert conference.name == "SEC"
        assert conference.gender == Gender.Female
        assert conference.urls.tds.endswith("/sec/cfid-1044")
        assert conference.ids.tds == "1044"
        assert conference.slug == "sec"

    def test_atlantic_coast(self, di_conferences_page):
        # Arrange
        target_id = "3"
        gender = Gender.Female

        # Act
        conference = di_conferences_page.get_conference_by_id(target_id, gender)

        # Assert
        assert conference is not None
        assert conference.name == "Atlantic Coast"
        assert conference.gender == Gender.Female
        assert conference.urls.tds.endswith("/atlantic-coast/cfid-3")
        assert conference.ids.tds == "3"
        assert conference.slug == "atlantic-coast"
