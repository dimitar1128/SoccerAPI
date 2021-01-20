"""team module
"""
import random
import logging
import names
from .constant.countries import *
from coolname import *

from database.soccer.models import *


def create_team(owner_id):
    """Create a team

    Create 3 goalkeepers, 6 defenders, 6 midfielders, 5 attackers
    Register created members to the team

    This generates team name, country name automatically

    Args:
        owner_id
            Id of user who would be the owner of the team
    Returns:
        True/False depend on the success of process
    """
    try:
        # pick one random country for the team
        country_idx = random.randint(0, len(countries))

        team = TBLTeam()
        team.owner_id = owner_id
        team.name = generate_slug(2)
        team.country = countries[country_idx]['name']
        team.save()

        # generate team members and register
        member_counts = {
            0: 3, # 3 goalkeeper
            1: 6, # 6 defender
            2: 6, # 6 midfielder
            3: 5, # 5 attackers
        }
        for type, count in member_counts.items():
            for i in range(count):
                ret = create_member(type, team)
                if not ret:
                    return False

        return True

    except Exception as e:
        logging.error(str(e))
        return False


def create_member(type, team_obj):
    """Create a member and register to team

    Generate human readable first name, last name for the player.
    Pick one random country and set to the player
    Generate random age from 18 to 40

    Args:
        type
            type of the member.
            0: Goalkeeper
            1: Defender
            2: Midfielder
            3: Attacker
        team_obj
            Team object which is the owner of the player
            (Pass team_obj instead of team_id to reduce accessing db time as
            this is a function to be called 20 times at once)
    Returns:
        True/False depend on the success of process
    """
    try:
        # pick one random country for the team
        country_idx = random.randint(0, len(countries))

        member = TBLMember()
        member.type = type
        member.first_name = names.get_first_name()
        member.last_name = names.get_last_name()
        member.country = countries[country_idx]['name']
        member.age = random.randint(18, 40)
        member.save()

        team_obj.members.add(member)
        team_obj.save()

        return True

    except Exception as e:
        logging.error(str(e))
        return False


def get_team_by_id(id):
    """Get team data by id

    Args:
        id
            Id of the team
    Returns:
        - when success
            Dictionary of team data including its members
        - when fail
            None
    """
    try:
        team = TBLTeam.objects.get(id=id)
        team_dict = {
            'id': team.id,
            'name': team.name,
            'country': team.country,
            'extra_value': team.extra_value,
            'members': []
        }
        for member in list(team.members.all().values()):
            if member['type'] == 0:
                member['type'] = 'Goal Keeper'
            elif member['type'] == 1:
                member['type'] = 'Defender'
            elif member['type'] == 2:
                member['type'] = 'Midfielder'
            elif member['type'] == 3:
                member['type'] = 'Attacker'

            team_dict['members'].append(member)

        return team_dict

    except Exception as e:
        return None