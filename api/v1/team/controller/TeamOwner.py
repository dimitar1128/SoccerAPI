from .base import *
from module.team import *
from module.user import *

class TeamOwner(viewsets.ViewSet):
    @token_required
    def list(self, request):
        """Get owner team information

        Url
            /team/my_team/
        Method
            GET
        Payload
            token (*)

        Returns:
            - when success
                Dictionary of team data including its members (HttpStatusCode = 200)
            - when fail
                Dictionary with code and message. Possible values are as following.
                    - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                    - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                    - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            user = get_user_with_token(
                request.POST.get('token')
            )
            if not user:
                return Response(RES_ERR_INTERNAL_SERVER, status=500)

            team_obj = TBLTeam.objects.get(owner_id = user.id)
            team = get_team_by_id(team_obj.id)
            if not team:
                return Response(RES_ERR_INTERNAL_SERVER, status=500)

            return Response(team, status=200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)

    @token_required
    def put(self, request):
        """Update team data including
                team name,
                team country,
                member first name,
                member last name
                member country.

        Url
            /team/my_team/
        Method
            PUT
        Payload
            token (*)
            team_name
            team_country

            member_id
            member_first_name
            member_last_name
            member_country

        at least one of team_name, team_country, member_id is required.
        If member_id is passed, at least one of member_first_name, member_last_name, member_country is required.

        Returns:
            Dictionary with code and message. Possible values are as following.
            - when success
                - RES_OK_TEAM_UPDATED           (HttpStatusCode = 200)
            - when fail
                - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                - RES_ERR_MISSING_FIELD         (HttpStatusCode = 400)
                - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            payload = request.POST

            user = get_user_with_token(
                payload.get('token')
            )
            if not user:
                return Response(RES_ERR_INTERNAL_SERVER, status=500)

            team_obj = TBLTeam.objects.get(owner_id=user.id)
            team_name = payload.get('team_name')
            team_country = payload.get('team_country')
            member_id = payload.get('member_id')
            member_first_name = payload.get('member_first_name')
            member_last_name = payload.get('member_last_name')
            member_country = payload.get('member_country')

            if (not team_name) and (not team_country) and (not member_id):
                return Response(RES_ERR_MISSING_FIELD, status=400)
            if member_id and (not member_first_name) and (not member_last_name) and (not member_country):
                return Response(RES_ERR_MISSING_FIELD, status=400)

            if member_id and user.is_superuser == 0 and len(team_obj.members.filter(id=member_id)) == 0:
                return Response(RES_ERR_INVALID_PERMISSION, status=401)

            if team_name:
                team_obj.name = team_name
                team_obj.save()
            if team_country:
                team_obj.country = team_country
                team_obj.save()

            if member_id:
                member = TBLMember.objects.get(id=member_id)
                if member_first_name:
                    member.first_name = member_first_name
                if member_last_name:
                    member.last_name = member_last_name
                if member_country:
                    member.country = member_country

                member.save()

            return Response(RES_OK_TEAM_UPDATED, status=200)


        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)

