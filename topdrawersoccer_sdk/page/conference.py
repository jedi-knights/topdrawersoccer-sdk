# from common.division import Division
# from common.gender import Gender
# from common.dao.club import ClubDAO
# from common.model.conference import Conference
# from common.model.player import Player
# from common.model.school import School
# from common.model.values import Values
# from common.utils import slugify, urljoin
# from page.object import PageObject
# from page.tds import config, utils
# from page.tds.team import TeamsPages
# from page.tds.utils import PREFIX, get_identifier_from_url
# from page.utils import get_href_from_anchor, get_text_from_anchor


from soccer_sdk_utils.gender import Gender
from soccer_sdk_utils.model.player import Player
from soccer_sdk_utils.model.values import Values
from soccer_sdk_utils.model.school import School
from soccer_sdk_utils.model.conference import Conference
from soccer_sdk_utils.page import PageObject
from soccer_sdk_utils.tools import urljoin, slugify
from soccer_sdk_utils.tools import get_href_from_anchor
from soccer_sdk_utils.tools import get_text_from_anchor

from soccer_sdk_utils.dao.club import ClubDAO

from soccer_sdk_utils.division import Division


from topdrawersoccer_sdk.constants import PREFIX
from topdrawersoccer_sdk.page.team import TeamsPages
from topdrawersoccer_sdk.utils import get_identifier_from_url


class ConferenceCommitmentsPage(PageObject):
    def __init__(
        self, gender: Gender, division: Division, conference_name: str, **kwargs
    ):
        super().__init__(**kwargs)

        conference = ConferencesPage(gender, division).get_conference_by_name(
            conference_name
        )

        self.gender = gender
        self.division = division

        self.url = urljoin(
            PREFIX, "/college-soccer/college-conferences/conference-details/"
        )

        if gender == Gender.Male:
            self.url = urljoin(self.url, "/men")
        else:
            self.url = urljoin(self.url, "/women")

        self.url = urljoin(self.url, f"/{conference.slug}")
        self.url = urljoin(self.url, f"/cfid-{conference.ids.tds}")
        self.url = urljoin(self.url, "tab-commitments")

        self.load()

    def get_commitments(self) -> list[Player]:
        """Returns a list of players who have committed to a school in the conference"""
        tables = self.soup.find_all(
            "table", class_=["table-striped", "tds-table", "female"]
        )

        body = None
        for table in tables:
            header = table.find("thead", class_="female")
            if header is not None:
                body = table.find("tbody")

        if body is None:
            return []

        players = []
        rows = body.find_all("tr")
        current_school = None
        for row in rows:
            columns = row.find_all("td")

            if len(columns) == 1:
                current_school = columns[0].text.strip()
                continue

            grad_year = columns[1].text.strip()
            name = get_text_from_anchor(columns[0])

            player = Player()
            player.gender = self.gender
            player.first_name = name.split(" ")[0] if name is not None else None
            player.last_name = name.split(" ")[-1] if name is not None else None
            player.club = columns[5].text.strip().replace("  ", " ")
            player.state = columns[4].text.strip()
            player.position = columns[2].text.strip()

            href = get_href_from_anchor(columns[0])
            if href is not None:
                url = urljoin(PREFIX, href)
                player.add_property("tds_url", url)

            player.add_property("city", columns[3].text.strip())
            player.add_property("grad_year", grad_year)
            player.add_property("commitment", current_school)
            player.add_property("league", ClubDAO().lookup_league(player.club))

            players.append(player)

        return players

    def get_commitments_by_year(self, year: str) -> list[Player]:
        """Returns a list of players who have committed to a school in the conference for a given year"""
        tables = self.soup.find_all(
            "table", class_=["table-striped", "tds-table", "female"]
        )

        body = None
        for table in tables:
            header = table.find("thead", class_="female")
            if header is not None:
                body = table.find("tbody")

        if body is None:
            return []

        players = []
        rows = body.find_all("tr")

        current_school = None
        for row in rows:
            columns = row.find_all("td")

            if len(columns) == 1:
                current_school = columns[0].text.strip()
                continue

            grad_year = columns[1].text.strip()

            if grad_year != year:
                continue

            name = get_text_from_anchor(columns[0])

            player = Player()
            player.gender = self.gender
            player.first_name = name.split(" ")[0] if name is not None else None
            player.last_name = name.split(" ")[-1] if name is not None else None
            player.club = columns[5].text.strip().replace("  ", " ")
            player.state = columns[4].text.strip()
            player.position = columns[2].text.strip()

            href = get_href_from_anchor(columns[0])
            if href is not None:
                url = urljoin(PREFIX, href)
                player.add_property("tds_url", url)
                player.add_property("tds_id", get_identifier_from_url(url))

            player.add_property("city", columns[3].text.strip())
            player.add_property("grad_year", grad_year)
            player.add_property("commitment", current_school)
            player.add_property("league", ClubDAO().lookup_league(player.club))

            players.append(player)

        return players


class SchoolCommitmentsPage(PageObject):
    def __init__(self, gender: Gender, name: str, **kwargs):
        super().__init__(**kwargs)

        self.gender = gender
        self.name = name
        self.clgid = kwargs.get("clgid", None)

        if self.clgid is None:
            self.clgid = TeamsPages().clgid_lookup(gender, name)

        self.url = urljoin(PREFIX, "/college-soccer/college-soccer-details")

        if gender == Gender.Male:
            self.url = urljoin(self.url, "/men")
        elif gender == Gender.Female:
            self.url = urljoin(self.url, "/women")
        else:
            raise ValueError(f"Unsupported gender {gender.name}!")

        self.url = urljoin(self.url, f"/{slugify(name)}")
        self.url = urljoin(self.url, f"/clgid-{self.clgid}")
        self.url = urljoin(self.url, "/tab-commitments")

        self.load()

    def get_commitments(self) -> list[Player]:
        """
        Note: The players leagues really need to be set properly before this method returns.
        OMC
        :return:
        """
        tables = self.soup.find_all(
            "table", class_=["table-striped", "tds-table", "female"]
        )

        body = None
        for table in tables:
            header = table.find("thead", class_="female")
            if header is not None:
                body = table.find("tbody")

        if body is None:
            return []

        players = []
        rows = body.find_all("tr")
        for row in rows:
            columns = row.find_all("td")

            if len(columns) == 1:
                continue

            grad_year = columns[1].text.strip()
            name = get_text_from_anchor(columns[0])

            player = Player()
            player.gender = self.gender
            player.first_name = name.split(" ")[0] if name is not None else None
            player.last_name = name.split(" ")[-1] if name is not None else None
            player.club = columns[5].text.strip().replace("  ", " ")
            player.state = columns[4].text.strip()
            player.position = columns[2].text.strip()

            href = get_href_from_anchor(columns[0])
            if href is not None:
                url = urljoin(PREFIX, href)
                player.add_property("tds_url", url)

            player.add_property("city", columns[3].text.strip())
            player.add_property("grad_year", grad_year)
            player.add_property("league", ClubDAO().lookup_league(player.club))

            players.append(player)

        return players

    def get_commitments_by_year(self, year: str) -> list[Player]:
        tables = self.soup.find_all(
            "table", class_=["table-striped", "tds-table", "female"]
        )

        body = None
        for table in tables:
            header = table.find("thead", class_="female")
            if header is not None:
                body = table.find("tbody")

        if body is None:
            return []

        players = []
        rows = body.find_all("tr")
        for row in rows:
            columns = row.find_all("td")

            grad_year = columns[1].text.strip()

            if grad_year != year:
                continue

            name = get_text_from_anchor(columns[0])

            player = Player()
            player.gender = self.gender
            player.first_name = name.split(" ")[0] if name is not None else None
            player.last_name = name.split(" ")[-1] if name is not None else None
            player.club = columns[5].text.strip().replace("  ", " ")
            player.state = columns[4].text.strip()
            player.position = columns[2].text.strip()

            href = get_href_from_anchor(columns[0])
            if href is not None:
                url = urljoin(PREFIX, href)
                player.add_property("tds_url", url)

            player.add_property("city", columns[3].text.strip())
            player.add_property("grad_year", grad_year)
            player.add_property("league", ClubDAO().lookup_league(player.club))

            players.append(player)

        return players


class ConferencePage(PageObject):
    def __init__(self, _conference: Conference, **kwargs):
        super().__init__(**kwargs)
        self.conference = _conference

    def schools(self) -> list:
        """Returns a list of schools in the conference"""
        schools = []

        self.load(self.conference.urls.tds)
        anchors = self.soup.find_all("a", class_=["player-name"])
        for anchor in anchors:
            school = School()
            school.name = get_text_from_anchor(anchor)
            school.gender = self.conference.gender
            school.urls = Values(
                tds=urljoin(config.BASE_URL, get_href_from_anchor(anchor))
            )
            school.ids = Values(tds=get_identifier_from_url(school.urls.tds))

            schools.append(school)

        return schools


class ConferencesPage(PageObject):
    def __init__(self, gender: Gender, division: Division, **kwargs):
        super().__init__(**kwargs)

        self.gender = gender
        self.division = division

        if division == Division.DI:
            self.url = urljoin(
                PREFIX, "/college-soccer/college-conferences/di/divisionid-1"
            )
        elif division == Division.DII:
            self.url = urljoin(
                PREFIX, "/college-soccer/college-conferences/dii/divisionid-2"
            )
        elif division == Division.DIII:
            self.url = urljoin(
                PREFIX, "/college-soccer/college-conferences/diii/divisionid-3"
            )
        elif division == Division.NAIA:
            self.url = urljoin(
                PREFIX, "/college-soccer/college-conferences/naia/divisionid-4"
            )
        elif division == Division.NJCAA:
            self.url = urljoin(
                PREFIX, "/college-soccer/college-conferences/njcaa/divisionid-5"
            )
        else:
            raise ValueError(f"Unsupported division {division.name}!")

        self.load()

    @property
    def gender(self) -> Gender:
        return self._gender

    @gender.setter
    def gender(self, value: Gender):
        self._gender = value

    @property
    def division(self) -> Division:
        return self._division

    @division.setter
    def division(self, value: Division):
        self._division = value

    def get_conference_by_name(self, name: str) -> Conference | None:
        conferences = self.get_conferences()

        for conference in conferences:
            if conference.name == name:
                return conference

        return None

    def get_conference_by_id(self, id: str) -> Conference | None:
        conferences = self.get_conferences(self.gender)

        for conference in conferences:
            if conference.ids.get("tds") == id:
                return conference

        return None

    def has_conference(self, name: str) -> bool:
        columns = self.soup.find_all("div", class_="col-lg-6")

        for column in columns:
            heading = column.find("div", class_=["heading-rectangle"])

            if heading is None:
                continue

            heading = heading.text.strip()

            if self.gender == Gender.Male and "Men's" not in heading:
                continue

            if self.gender == Gender.Female and "Women's" not in heading:
                continue

            table = column.find("table", class_=["table_stripped", "tds_table"])
            cells = table.find_all("td")

            for cell in cells:
                current_conference_name = get_text_from_anchor(cell)

                if current_conference_name == name:
                    return True

        return False

    def get_conferences(self):
        conferences = []

        columns = self.soup.find_all("div", class_="col-lg-6")

        for column in columns:
            heading = column.find("div", class_=["heading-rectangle"])

            if heading is None:
                continue

            heading = heading.text.strip()

            if self.gender == Gender.Male and "Men's" not in heading:
                continue

            if self.gender == Gender.Female and "Women's" not in heading:
                continue

            table = column.find("table", class_=["table_stripped", "tds_table"])
            cells = table.find_all("td")

            for cell in cells:
                anchor = cell.find("a")
                href = get_href_from_anchor(anchor)

                conference = Conference()

                conference.name = get_text_from_anchor(anchor)
                conference.division = self.division
                conference.gender = self.gender

                conference.ids = Values()
                conference.urls = Values()

                conference.urls.tds = urljoin(PREFIX, href)
                conference.ids.tds = str(get_identifier_from_url(href))

                conferences.append(conference)

        return conferences

    @staticmethod
    def get_division_by_conference_name(gender: Gender, name: str) -> Division | None:
        for division in Division:
            if division == Division.All:
                continue

            if ConferencesPage(gender, division).has_conference(name):
                return division

        return None


if __name__ == "__main__":
    import sys
    from os import path
    from dotenv import load_dotenv

    load_dotenv(path.join(sys.path[1], ".env"))

    division = ConferencesPage.get_division_by_conference_name(
        Gender.Female, "West Coast"
    )
    print(division)

    division = ConferencesPage.get_division_by_conference_name(
        Gender.Female, "Conference Carolinas"
    )
    print(division)

    division = ConferencesPage.get_division_by_conference_name(
        Gender.Female, "Centennial"
    )
    print(division)

    division = ConferencesPage.get_division_by_conference_name(
        Gender.Female, "California Pacific"
    )
    print(division)

    division = ConferencesPage.get_division_by_conference_name(
        Gender.Female, "Central Valley"
    )
    print(division)

    print()
    print("West Cost Conference Commitments")
    page = ConferenceCommitmentsPage(Gender.Female, Division.DI, "West Coast")

    players = page.get_commitments()

    for player in players:
        print(player)


    print()
    print("Santa Clara Commitments")
    page = SchoolCommitmentsPage(Gender.Female, "Santa Clara", clgid=474)

    players = page.get_commitments_by_year("2023")

    for player in players:
        print(player)
