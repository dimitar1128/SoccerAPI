from .base import *
from module.team import *
from module.user import *

class Team(viewsets.ViewSet):
    @administrator_func
    def list(self, request):
        """List all team

        (This api is for administrator)

        Url
            /team/
        Method
            GET
        Payload
            token (*)

        Returns:
            - when success
                List of dictionary of team's data (HttpStatusCode = 200)
            - when fail
                Dictionary with code and message. Possible values are as following.
                    - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                    - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                    - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                    - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            res = []
            teams = list(TBLTeam.objects.all())
            for team in teams:
                res.append(get_team_from_obj(team))

            return Response(res, status=200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)

    @administrator_func
    def create(self, request):
        """Create a team

        (This api is for administrator)

        Url
            /team/
        Method
            POST
        Payload
            token (*)
            name
            country
            extra_value

        Returns:
            Dictionary with code and message. Possible values are as following.
            - when success
                - RES_OK_TEAM_CREATED           (HttpStatusCode = 201)
                *** team id will be added in team_id field
            - when fail
                - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                - RES_ERR_INVALID_FILED         (HttpStatusCode = 400)
                - RES_ERR_TEAM_CREATE           (HttpStatusCode = 500)
                - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            # check payload
            payload = request.POST
            exp_args = [
                {
                    'field': 'name',
                    'required': False,
                    'type': 'string',
                },
                {
                    'field': 'country',
                    'required': False,
                    'type': 'string'
                },
                {
                    'field': 'extra_value',
                    'required': False,
                    'type': 'float',
                }
            ]
            ret = check_payloads(exp_args, payload)
            if ret == -1:
                return Response(RES_ERR_MISSING_FIELD, status=400)
            elif ret == -2:
                return Response(RES_ERR_INVALID_FILED, status=400)

            name = payload.get('name')
            country = payload.get('country')
            extra_value = payload.get('extra_value')

            if extra_value:
                extra_value = float(extra_value)

            # create team
            team_id = create_team(
                None,
                name,
                country,
                extra_value
            )
            if not team_id:
                return Response(RES_ERR_TEAM_CREATE, status=500)

            ret = RES_OK_TEAM_CREATED
            ret['team_id'] = team_id
            return Response(ret, status=201)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)


    @administrator_func
    def put(self, request):
        """Update team

        (This api is for administrator)

        Url
            /team/
        Method
            PUT
        Payload
            token (*)
            id (*)
                Team id to be updated
            name
            country
            extra_value

            *Note: At least one of name, country, extra_value should be provided
        Returns:
            Dictionary with code and message. Possible values are as following.
            - when success
                - RES_OK_TEAM_UPDATED           (HttpStatusCode = 200)
            - when fail
                - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                - RES_ERR_MISSING_FIELD         (HttpStatusCode = 400)
                - RES_ERR_INVALID_FILED         (HttpStatusCode = 400)
                - RES_ERR_TEAM_NOT_EXIST        (HttpStatusCode = 400)
                - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            # payload check
            payload = request.POST
            exp_args = [
                {
                    'field': 'id',
                    'required': True,
                    'type': 'integer',
                },
                {
                    'field': 'name',
                    'required': False,
                    'type': 'string',
                },
                {
                    'field': 'country',
                    'required': False,
                    'type': 'string'
                },
                {
                    'field': 'extra_value',
                    'required': False,
                    'type': 'float',
                }
            ]
            ret = check_payloads(exp_args, payload)
            if ret == -1:
                return Response(RES_ERR_MISSING_FIELD, status=400)
            elif ret == -2:
                return Response(RES_ERR_INVALID_FILED, status=400)

            # if all name, country, extra value are not provided
            name = payload.get('name')
            country = payload.get('country')
            extra_value = payload.get('extra_value')
            if (not name) and (not country) and (not extra_value):
                return Response(RES_ERR_MISSING_FIELD, status=400)

            team_id = int(payload['id'])

            # if team does not exist
            if len(TBLTeam.objects.filter(id=team_id)) == 0:
                return Response(RES_ERR_TEAM_NOT_EXIST, status=400)

            # update team
            team = TBLTeam.objects.get(id=team_id)
            if name:
                team.name = name
            if country:
                team.country = country
            if extra_value:
                team.extra_value = float(extra_value)

            team.save()

            return Response(RES_OK_TEAM_UPDATED, status=200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)


    @administrator_func
    def delete(self, request):
        """Delete team

        (This api is for administrator)

        Url
            /team/
        Method
            PUT
        Payload
            token (*)
            id (*)
                Team id to be updated
        Returns:
            Dictionary with code and message. Possible values are as following.
            - when success
                - RES_OK_TEAM_DELETED           (HttpStatusCode = 204)
            - when fail
                - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                - RES_ERR_MISSING_FIELD         (HttpStatusCode = 400)
                - RES_ERR_INVALID_FILED         (HttpStatusCode = 400)
                - RES_ERR_TEAM_NOT_EXIST        (HttpStatusCode = 400)
                - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            # payload check
            payload = request.POST
            exp_args = [
                {
                    'field': 'id',
                    'required': True,
                    'type': 'integer',
                }
            ]
            ret = check_payloads(exp_args, payload)
            if ret == -1:
                return Response(RES_ERR_MISSING_FIELD, status=400)
            elif ret == -2:
                return Response(RES_ERR_INVALID_FILED, status=400)

            team_id = int(payload['id'])

            # if team does not exist
            if len(TBLTeam.objects.filter(id=team_id)) == 0:
                return Response(RES_ERR_TEAM_NOT_EXIST, status=400)

            # delete team
            team = TBLTeam.objects.get(id=team_id)
            team.delete()

            return Response(RES_OK_TEAM_DELETED, status=204)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)