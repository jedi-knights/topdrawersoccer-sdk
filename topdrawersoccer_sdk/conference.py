from urllib.parse import urljoin

from soccer_sdk_utils.page import PageObject
from soccer_sdk_utils.gender import Gender

from topdrawersoccer_sdk.division import Division
from topdrawersoccer_sdk.constants import PREFIX


def division_to_conference_url(division: Division) -> str:
    """
    Retrieve the conference URL for a given division.

    :param division:
    :return:
    """
    if division == Division.DI:
        return urljoin(PREFIX, "college-soccer/college-conferences/di/divisionid-1")

    if division == Division.DII:
        return urljoin(PREFIX, "college-soccer/college-conferences/dii/divisionid-2")

    if division == Division.DIII:
        return urljoin(PREFIX, "college-soccer/college-conferences/diii/divisionid-3")

    if division == Division.NAIA:
        return urljoin(PREFIX, "college-soccer/college-conferences/naia/divisionid-4")

    if division == Division.NJCAA:
        return urljoin(PREFIX, "college-soccer/college-conferences/njcaa/divisionid-5")

    raise ValueError(f"Unsupported division '{division}'")


class ConferencePage(PageObject):
    def __init__(self):
        pass

class ConferencesPage(PageObject):
    def __init__(self, gender: Gender, division: Division, **kwargs):
        pass

    def get_conferences(self) -> list[Conference]:
        pass