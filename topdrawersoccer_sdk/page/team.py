from http import HTTPStatus

from soccer_sdk_utils.division import Division, DivisionList
from soccer_sdk_utils.gender import Gender, string_to_gender
from soccer_sdk_utils.model.conference import Conference
from soccer_sdk_utils.model.school import School
from soccer_sdk_utils.tools import urljoin
from soccer_sdk_utils.page import PageObject
# from page.tds import config, utils
from soccer_sdk_utils.tools import get_href_from_anchor, get_text_from_anchor

from topdrawersoccer_sdk.constants import PREFIX
from topdrawersoccer_sdk.utils import url_to_gender, get_identifier_from_url

URL_MAPPING = {"di"}


class TeamsPage(PageObject):
    def __init__(self, gender: Gender, division: Division, **kwargs):
        super().__init__(**kwargs)

        self.gender = gender
        self.division = division

        if self.division == Division.DI:
            self.url = "https://www.topdrawersoccer.com/college/teams/?divisionName=di&divisionId=1"
        elif self.division == Division.DII:
            self.url = "https://www.topdrawersoccer.com/college/teams/?divisionName=dii&divisionId=2"
        elif self.division == Division.DIII:
            self.url = "https://www.topdrawersoccer.com/college/teams/?divisionName=diii&divisionId=3"
        elif self.division == Division.NAIA:
            self.url = "https://www.topdrawersoccer.com/college/teams/?divisionName=naia&divisionId=4"
        elif self.division == Division.NJCAA:
            self.url = "https://www.topdrawersoccer.com/college/teams/?divisionName=njcaa&divisionId=5"
        else:
            raise ValueError(f"Invalid division: {self.division}")

        # self.url = urljoin(config.BASE_URL, f"college/teams/?{repr(division)}")

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

    def conference_names(self):
        conference_names = []

        if self.status_code != HTTPStatus.OK:
            raise ValueError(f"Failed to get teams page: {self.status_code}")

        tables = self.soup.find_all("table", class_=["table-striped", "tds-table"])

        for table in tables:
            conference_name = table.find("caption").text
            conference_names.append(conference_name)

        conference_names.sort()

        return conference_names

    def get_conferences(self) -> list[Conference]:
        conferences = []

        if self.status_code != HTTPStatus.OK:
            raise ValueError(f"Failed to get teams page: {self.status_code}")

        tables = self.soup.find_all("table", class_=["table-striped", "tds-table"])

        for table in tables:
            caption_tag = table.find("caption")

            text = get_text_from_anchor(caption_tag)
            href = get_href_from_anchor(caption_tag)

            url = urljoin(PREFIX, href)
            tds_id = get_identifier_from_url(url)

            conference = Conference()
            conference.gender = self.gender
            conference.name = text
            conference.division = self.division
            conference.urls.tds = url
            conference.ids.tds = tds_id

            conferences.append(conference)

        return conferences

    def get_conference_by_name(self, conference_name: str) -> Conference | None:
        if self.status_code != HTTPStatus.OK:
            raise ValueError(f"Failed to get teams page: {self.status_code}")

        tables = self.soup.find_all("table", class_=["table-striped", "tds-table"])

        for table in tables:
            caption_tag = table.find("caption")

            name = get_text_from_anchor(caption_tag)

            if name != conference_name:
                continue

            conference = Conference()
            conference.name = name
            conference.gender = self.gender
            conference.division = self.division
            conference.urls.tds = urljoin(
                PREFIX, get_href_from_anchor(caption_tag)
            )
            conference.ids.tds = get_identifier_from_url(conference.urls.tds)

            return conference

        return None

    def get_schools_by_conference(self, target_conference_name: str) -> list[School]:
        schools = []

        if self.status_code != HTTPStatus.OK:
            raise ValueError(f"Failed to get teams page: {self.status_code}")

        tables = self.soup.find_all("table", class_=["table-striped", "tds-table"])

        for table in tables:
            caption_tag = table.find("caption")

            conference_name = get_text_from_anchor(caption_tag)

            if conference_name != target_conference_name:
                continue

            rows = table.find_all("tr")
            for row in rows:
                column = row.find("td")

                href = get_href_from_anchor(column)

                buffer = url_to_gender(href)
                href_gender = string_to_gender(buffer)

                if href_gender != self.gender:
                    continue

                href_id = get_identifier_from_url(href)

                school = School()
                school.name = get_text_from_anchor(column)
                school.urls.tds = urljoin(PREFIX, href)
                school.ids.tds = href_id
                school.gender = href_gender

                schools.append(school)

        return schools


class TeamsPages:
    def __init__(self):
        pass

    def clgid_lookup(self, gender: Gender, school_name: str):
        for division in DivisionList:
            teams_page = TeamsPage(gender, division)
            conferences = teams_page.get_conferences()

            for conference in conferences:
                schools = teams_page.get_schools_by_conference(conference.name)
                for school in schools:
                    if school.name != school_name:
                        continue

                    if school.gender != gender:
                        continue

                    return school.ids.tds

        return None

    def division_by_conference_name(self, conference_name: str):
        for division in DivisionList:
            conferences = TeamsPage(division).get_conferences()

            for name, conference_data in conferences.items():
                if name == conference_name:
                    return division

        return None

    def conference_names(self, gender: Gender):
        conference_names = []

        for division in DivisionList:
            page = self.pages[division.name]
            conference_names.extend(page.conference_names())

        return conference_names

    def school_names(self, gender: Gender):
        conferences = self.conference_names()

        school_names = []
        for conference in conferences:
            schools = self.school_names_by_conference(conference)
            school_names.extend(schools)

    def schools_by_conference_name(self, gender: Gender, conference_name: str):
        for division in DivisionList:
            page = self.pages[division.name]

            tables = page.soup.find_all("table", class_=["table-striped", "tds-table"])

            for table in tables:
                schools = []

                caption_tag = table.find("caption")
                current_conference_name = get_text_from_anchor(caption_tag)

                if current_conference_name != conference_name:
                    continue

                rows = table.find_all("tr")
                for row in rows:
                    column = row.find("td")

                    href = get_href_from_anchor(column)

                    if string_to_gender(url_to_gender(href)) != gender:
                        continue

                    school = School()
                    school.gender = gender
                    school.name = get_text_from_anchor(column)
                    school.urls.tds = href
                    school.ids.tds = get_identifier_from_url(school.urls.tds)

                    schools.append(school)

                return schools

        return None


if __name__ == "__main__":
    page = TeamsPage(Gender.Female, Division.DI)

    # conference = page.get_conference_by_name("West Coast")
    # print(conference)

    conferences = page.get_conferences()
    schools = page.get_schools_by_conference("West Coast")

    for school in schools:
        print(school)

    # clgid = TeamsPages().clgid_lookup(Gender.Female, "Santa Clara")
    #
    # print(clgid)

    # teams_page = TeamsPage(Division.DI)
    #
    # conference_names = teams_page.get_conference_names()
    #
    # conferences = teams_page.get_conferences()
    #
    # for name in conferences:
    #     container = conferences.get(name)
    #     conference = container.get("conference")
    #     schools = container.get("schools")
    #
    #     for school in schools:
    #         print(f"{conference.name} - {school.name} - {school.urls.tds}")

    # female_schools = get_schools_by_conference_name(Gender.Female, "West Coast")
    # male_schools = get_schools_by_conference_name(Gender.Male, "West Coast")
    #
    # for school in female_schools:
    #     print(f"{school.name} - {school.urls.tds}")

    # print(get_division_by_conference_name("Central Atlantic Conference"))

    # pages = TeamsPages()
    #
    # school_name = "South Carolina"
    # female_clgid = pages.clgid_lookup(Gender.Female, school_name)
    # male_clgid = pages.clgid_lookup(Gender.Male, school_name)
    #
    # print(school_name)
    # print(f"Men: {male_clgid}")
    # print(f"Women: {female_clgid}")
    #
    # print()
    #
    # print("ASUN: " + str(pages.division_by_conference_name("ASUN")))
    # print("West Coast: " + str(pages.division_by_conference_name("West Coast")))
    # print("Atlantic Coast: " + str(pages.division_by_conference_name("Atlantic Coast")))
    # print("Central Atlantic Conference: " + str(pages.division_by_conference_name("Central Atlantic Conference")))
    # print("American Southwest: " + str(pages.division_by_conference_name("American Southwest")))
    # print("Allegheny Mountain: " + str(pages.division_by_conference_name("Allegheny Mountain")))
    # print("Kentucky Intercollegiate: " + str(pages.division_by_conference_name("Kentucky Intercollegiate")))
    #
    #
    # print("\n\nSchools By Conference Name")
    # print("ASUN")
    # for school in pages.schools_by_conference_name(Gender.Female, "ASUN"):
    #     print(f"  {school}")
    #
    # print("\nWest Coast")
    # for school in pages.schools_by_conference_name(Gender.Female, "West Coast"):
    #     print(f"  {school}")
    #
    # print("\nSEC")
    # for school in pages.schools_by_conference_name(Gender.Female, "SEC"):
    #     print(f"  {school}")
    #
    # print("\nAtlantic Coast")
    # for school in pages.schools_by_conference_name(Gender.Female, "Atlantic Coast"):
    #     print(f"  {school}")
