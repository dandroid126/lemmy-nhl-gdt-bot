from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, EnumMeta


@dataclass
class Team:
    id: int
    abbreviation: str
    city: str
    name: str
    logo_url: str

    def get_logo_markdown(self):
        """
        Return the Markdown string for displaying the logo.

        Returns:
            str: The Markdown string with the logo image.
        """
        return f'![{self.abbreviation}]({self.logo_url})'

    def get_team_table_entry(self):
        """
        Generates a table entry for the team.

        Returns:
            str: The table entry for the team, including the team logo and abbreviation.
        """
        # Get the team logo in Markdown format
        logo_markdown = self.get_logo_markdown()

        # Combine the logo markdown and team abbreviation
        table_entry = f"{logo_markdown} {self.abbreviation}"

        return table_entry

    def __eq__(self, other: Team):
        return self.id == other.id


class TeamsEnumMeta(EnumMeta):

    def __getitem__(self, item):
        if item not in Teams.__members__:
            return Teams.ERR
        return super().__getitem__(item)


class Teams(Enum, metaclass=TeamsEnumMeta):
    NJD = Team(1, 'NJD', 'New Jersey', 'Devils', 'https://lemmy.ca/pictrs/image/eb1a001e-6e70-4cee-b412-6ffc41755d51.png')
    NYI = Team(2, 'NYI', 'New York', 'Islanders', 'https://lemmy.ca/pictrs/image/9901d131-6f32-4bc2-8013-6a1037c1d4db.png')
    NYR = Team(3, 'NYR', 'New York', 'Rangers', 'https://lemmy.ca/pictrs/image/7061371d-fe61-4237-bf32-fa68b2a316cd.png')
    PHI = Team(4, 'PHI', 'Philadelphia', 'Flyers', 'https://lemmy.ca/pictrs/image/8866c84a-e374-42f6-aab5-8184c0612e0d.png')
    PIT = Team(5, 'PIT', 'Pittsburgh', 'Penguins', 'https://lemmy.ca/pictrs/image/3b955364-fc3a-4a6e-b2b1-2b3cd062b4c0.png')
    BOS = Team(6, 'BOS', 'Boston', 'Bruins', 'https://lemmy.ca/pictrs/image/4625ed3e-4a81-4e2d-9db9-18b52b0cc2a6.png')
    BUF = Team(7, 'BUF', 'Buffalo', 'Sabres', 'https://lemmy.ca/pictrs/image/7c7d2a09-9283-4b2c-b66a-902ce43e4c6f.png')
    MTL = Team(8, 'MTL', 'Montréal', 'Canadiens', 'https://lemmy.ca/pictrs/image/4d9a1fc9-e62d-4ecf-9218-cf3017b30f75.png')
    OTT = Team(9, 'OTT', 'Ottawa', 'Senators', 'https://lemmy.ca/pictrs/image/5e2c941c-23a7-49c3-aadd-76913f1d87c3.png')
    TOR = Team(10, 'TOR', 'Toronto Maple', 'Leafs', 'https://lemmy.ca/pictrs/image/d072c25d-491e-4c38-acb7-7b313e66694d.png')
    CAR = Team(12, 'CAR', 'Carolina', 'Hurricanes', 'https://lemmy.ca/pictrs/image/b37d627b-c321-42dd-bc1e-c760efee3400.png')
    FLA = Team(13, 'FLA', 'Florida', 'Panthers', 'https://lemmy.ca/pictrs/image/3475a4e4-4941-40b3-91e3-9a3157a3eed2.png')
    TBL = Team(14, 'TBL', 'Tampa Bay', 'Lightning', 'https://lemmy.ca/pictrs/image/303d7183-54ac-403e-9917-d2cb59657aaf.png')
    WSH = Team(15, 'WSH', 'Washington', 'Capitals', 'https://lemmy.ca/pictrs/image/045d8587-6591-4ab6-8414-819cfcea5029.png')
    CHI = Team(16, 'CHI', 'Chicago', 'Blackhawks', 'https://lemmy.ca/pictrs/image/fdb4d79b-b6c7-495f-b936-36a5a95b27c0.png')
    DET = Team(17, 'DET', 'Detroit', 'Red Wings', 'https://lemmy.ca/pictrs/image/7c482335-5915-4e46-86fe-64f0839e7367.png')
    NSH = Team(18, 'NSH', 'Nashville', 'Predators', 'https://lemmy.ca/pictrs/image/f4556171-a3a4-4f10-98ce-4764ff897444.png')
    STL = Team(19, 'STL', 'St. Louis', 'Blues', 'https://lemmy.ca/pictrs/image/d287c13b-d74e-4050-bbab-c7061b62bf4c.png')
    CGY = Team(20, 'CGY', 'Calgary', 'Flames', 'https://lemmy.ca/pictrs/image/1a7a673a-810a-4254-8280-348985c2c57e.png')
    COL = Team(21, 'COL', 'Colorado', 'Avalanche', 'https://lemmy.ca/pictrs/image/3061fba5-f972-42b2-a89e-2c57ab0dabd6.png')
    EDM = Team(22, 'EDM', 'Edmonton', 'Oilers', 'https://lemmy.ca/pictrs/image/b777f4cf-da58-421a-88fc-682a11d6105a.png')
    VAN = Team(23, 'VAN', 'Vancouver', 'Canucks', 'https://lemmy.ca/pictrs/image/a65aa2c0-f5d5-4c6c-8bbe-09c35aebff6f.png')
    ANA = Team(24, 'ANA', 'Anaheim', 'Ducks', 'https://lemmy.ca/pictrs/image/9efd8b21-3414-4e4f-8be3-559809ec133a.png')
    DAL = Team(25, 'DAL', 'Dallas', 'Stars', 'https://lemmy.ca/pictrs/image/dade02ae-46d7-4f66-b38e-0e280dce2081.png')
    LAK = Team(26, 'LAK', 'Los Angeles', 'Kings', 'https://lemmy.ca/pictrs/image/ffa7e866-dd9a-430b-a3a1-61ef62dff3d9.png')
    SJS = Team(28, 'SJS', 'San Jose', 'Sharks', 'https://lemmy.ca/pictrs/image/a278e5aa-6f6f-4cdb-a0dc-03630b03a3a9.png')
    CBJ = Team(29, 'CBJ', 'Columbus', 'Blue Jackets', 'https://lemmy.ca/pictrs/image/af857875-5612-47f7-8015-01b431cb2044.png')
    MIN = Team(30, 'MIN', 'Minnesota', 'Wild', 'https://lemmy.ca/pictrs/image/a54a2083-557e-4e54-8343-329e31aa09c6.png')
    WPG = Team(52, 'WPG', 'Winnipeg', 'Jets', 'https://lemmy.ca/pictrs/image/b0dd50ff-5d09-4ca2-b846-150ca37d92ab.png')
    ARI = Team(53, 'ARI', 'Arizona', 'Coyotes', 'https://lemmy.ca/pictrs/image/c700df7c-41d6-405b-81c2-7b7610aa400b.png')
    VGK = Team(54, 'VGK', 'Vegas', 'Golden Knights', 'https://lemmy.ca/pictrs/image/20aaabff-312a-437f-8247-825fc137d33e.png')
    SEA = Team(55, 'SEA', 'Seattle', 'Kraken', 'https://lemmy.ca/pictrs/image/e8edb628-f3a4-40df-b6a0-7752152ad7b3.png')
    ERR = Team(0, 'ERR', 'Error', 'Error', '')

    @staticmethod
    def get_all_teams() -> list[Team]:
        """
        Returns a list of all teams.

        :return: A list of Team objects representing all the teams.
        :rtype: list[Team]
        """
        return [team.value for team in Teams]


_team_id_map = {}
for _team in Teams.get_all_teams():
    _team_id_map[_team.id] = _team


def get_team_from_id(team_id: int) -> Team:
    """
    Retrieve the Team object corresponding to the given team_id.

    Args:
        team_id (int): The ID of the team to retrieve.

    Returns:
        Team: The Team object corresponding to the given team_id, or None if not found.
    """
    return _team_id_map.get(team_id, None)
