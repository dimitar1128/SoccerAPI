"""team module
"""
from database.soccer.models import *

def create_team(owner_id, team_name, team_country):
    """Create a team

    Create 3 goalkeepers, 6 defenders, 6 midfielders, 5 attackers
    Register created members to the team

    Args:
        owner_id
            Id of user who would be the owner of the team
        team_name
            Name of the team. Should be less than 100 letters
        team_country
            Country of the team. Shoud be less than 50 letters
    Returns:
    """
    team = TBLTeam()
    team.owner_id = owner_id
    team.name = team_name
    team.country = team_country
