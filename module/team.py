"""team module
"""
import random
import logging
import names
import time
from .constant.countries import *
from coolname import *

from database.soccer.models import *


def create_team(owner_id, name=None, country=None, extra_value=None):
    """Create a team

    Create 3 goalkeepers, 6 defenders, 6 midfielders, 5 attackers
    Register created members to the team

    This generates team name, country name automatically

    Args:
        owner_id
            Id of user who would be the owner of the team
            This value can be none for no owner
        name
            (optional) if not passed, it will generate auto name
        country
            (optional) if not passed, it will generate auto country
        extra_value
            (optional) if not passed, it will set default value
    Returns:
        Team id when success
        None when fail
    """
    try:
        # pick one random country for the team
        country_idx = random.randint(0, len(countries))

        team = TBLTeam()
        team.owner_id = owner_id
        team.name = generate_slug(2) if not name else name
        team.country = countries[country_idx]['name'] if not country else country
        if extra_value:
            team.extra_value = extra_value
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
                member_id = create_member(type, team)
                if not member_id:
                    return None

                time.sleep(0.1)

        return team.id

    except Exception as e:
        logging.error(str(e))
        return None


def create_member(type=None, team_obj=None, first_name=None, last_name=None, country=None, age=None, value=None):
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
        first_name
        last_name
        country
        age
        value

        **Note: all of these arguments are optional, if it is not passed, it will generate automatic values except team_id.
        If team_id is not passed, it will put None value which means it is not included in any teams.
    Returns:
        Member id when success
        None when fail

    """
    try:
        # pick one random country for the team
        country_idx = random.randint(0, len(countries) - 1)

        member = TBLMember()
        member.type = type if type != None else random.randint(0, 3)
        member.first_name = names.get_first_name() if not first_name else first_name
        member.last_name = names.get_last_name() if not last_name else last_name
        member.country = countries[country_idx]['name'] if not country else country
        member.age = random.randint(18, 40) if not age else age
        member.team_id = team_obj.id if team_obj else None
        if value:
            member.value = value
        member.save()

        if team_obj:
            team_obj.members.add(member)
            team_obj.save()

        return member.id

    except Exception as e:
        logging.error(str(e))
        return None


def get_team_from_obj(team):
    """Get team data from its object

    Args:
        team
            team object
    Returns:
        - when success
            Dictionary of team data including its members
        - when fail
            None
    """
    try:
        team_dict = {
            'id': team.id,
            'owner_id': team.owner_id,
            'name': team.name,
            'country': team.country,
            'extra_value': team.extra_value,
            'total_value': 0,
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

            team_dict['total_value'] += member['value']
            team_dict['members'].append(member)

        return team_dict

    except Exception as e:
        return None