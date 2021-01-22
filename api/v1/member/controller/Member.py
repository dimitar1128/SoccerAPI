from .base import *
from module.team import *

class Member(viewsets.ViewSet):
    @administrator_func
    def list(self, request):
        """List all members

        (This api is for administrator)

        Url
            /member/
        Method
            GET
        Payload
            token (*)

        Returns:
            - when success
                List of dictionary of member's data (HttpStatusCode = 200)
            - when fail
                Dictionary with code and message. Possible values are as following.
                    - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                    - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                    - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                    - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            res = []
            members = list(TBLMember.objects.all().values())
            for member in members:
                if member['type'] == 0:
                    member['type'] = 'Goal Keeper'
                elif member['type'] == 1:
                    member['type'] = 'Defender'
                elif member['type'] == 2:
                    member['type'] = 'Midfielder'
                elif member['type'] == 3:
                    member['type'] = 'Attacker'

                res.append(member)

            return Response(res, status=200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)

    @administrator_func
    def create(self, request):
        """Create a member

        (This api is for administrator)

        Url
            /member/
        Method
            POST
        Payload
            token (*)
            first_name
            last_name
            country
            age
            type
            value
            team_id
                Team id to register the member.
            market_price
                If this field is passed, the member will be set on the transfer list.
        Returns:
            Dictionary with code and message. Possible values are as following.
            - when success
                -> if team_id, market_price is passed
                    RES_OK_NEW_MEMBER_REGISTERED_TO_TEAM_AND_MARKET (HttpStatusCode = 201)
                -> else if team_id is passed
                    - RES_OK_NEW_MEMBER_REGISTERED_TO_TEAM          (HttpStatusCode = 201)
                -> else if market_price is passed
                    - RES_OK_NEW_MEMBER_REGISTERED_TO_MARKET        (HttpStatusCode = 201)
                -> else if team_id is not passed
                    - RES_OK_MEMBER_CREATED                         (HttpStatusCode = 201)

                *** member id will be added in member_id field
            - when fail
                - RES_ERR_TOKEN_REQUIRED                        (HttpStatusCode = 401)
                - RES_ERR_INVALID_TOKEN                         (HttpStatusCode = 401)
                - RES_ERR_INVALID_PERMISSION                    (HttpStatusCode = 401)
                - RES_ERR_INVALID_FILED                         (HttpStatusCode = 400)
                - RES_ERR_TEAM_NOT_EXIST                        (HttpStatusCode = 400)
                - RES_ERR_INTERNAL_SERVER                       (HttpStatusCode = 500)
        """
        try:
            # check payload
            payload = request.POST
            exp_args = [
                {
                    'field': 'first_name',
                    'required': False,
                    'type': 'string',
                },
                {
                    'field': 'last_name',
                    'required': False,
                    'type': 'string',
                },
                {
                    'field': 'country',
                    'required': False,
                    'type': 'string'
                },
                {
                    'field': 'age',
                    'required': False,
                    'type': 'integer',
                },
                {
                    'field': 'type',
                    'required': False,
                    'type': 'integer',
                },
                {
                    'field': 'value',
                    'required': False,
                    'type': 'float',
                },
                {
                    'field': 'team_id',
                    'required': False,
                    'type': 'integer',
                },
                {
                    'field': 'market_price',
                    'required': False,
                    'type': 'float',
                }
            ]
            ret = check_payloads(exp_args, payload)
            if ret == -1:
                return Response(RES_ERR_MISSING_FIELD, status=400)
            elif ret == -2:
                return Response(RES_ERR_INVALID_FILED, status=400)

            first_name = payload.get('first_name')
            last_name = payload.get('last_name')
            country = payload.get('country')
            age = payload.get('age')
            type = payload.get('type')
            value = payload.get('value')
            team_id = payload.get('team_id')
            market_price = payload.get('market_price')

            if age:
                age = int(age)
                if age < 18 or age > 40:
                    return Response(RES_ERR_INVALID_FILED, status=400)

            if type:
                type = int(type)
                if type < 0 or type > 3:
                    return Response(RES_ERR_INVALID_FILED, status=400)

            if value:
                value = float(value)

            team_obj = None
            if team_id:
                team_id = int(team_id)
                if len(TBLTeam.objects.filter(id=team_id)) == 0:
                    return Response(RES_ERR_TEAM_NOT_EXIST, status=400)
                team_obj = TBLTeam.objects.get(id=team_id)

            # create member
            member_id = create_member(
                type,
                team_obj,
                first_name,
                last_name,
                country,
                age,
                value
            )
            if not member_id:
                return Response(RES_ERR_INTERNAL_SERVER, 500)

            if market_price != None:
                market = TBLMarket()
                market.member_id = member_id
                market.price = market_price
                market.save()

            if team_obj and market_price != None:
                ret = RES_OK_NEW_MEMBER_REGISTERED_TO_TEAM_AND_MARKET
            elif team_obj:
                ret = RES_OK_NEW_MEMBER_REGISTERED_TO_TEAM
            elif market_price:
                ret = RES_OK_NEW_MEMBER_REGISTERED_TO_MARKET
            else:
                ret = RES_OK_MEMBER_CREATED

            ret['member_id'] = member_id
            return Response(ret, status=201)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)

    @administrator_func
    def put(self, request):
        """Update a member

        (This api is for administrator)

        Url
            /member/
        Method
            PUT
        Payload
            token (*)
            id (*)
                Id of member to be updated
            first_name
            last_name
            country
            age
            type
            value

            **Note; at least one of above should be passed
        Returns:
            Dictionary with code and message. Possible values are as following.
            - when success
                - RES_OK_MEMBER_UPDATED         (HttpStatusCode = 200)
            - when fail
                - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                - RES_ERR_MISSING_FIELD         (HttpStatusCode = 400)
                - RES_ERR_INVALID_FILED         (HttpStatusCode = 400)
                - RES_ERR_MEMBER_NOT_EXIST      (HttpStatusCode = 400)
                - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            # check payload
            payload = request.POST
            exp_args = [
                {
                    'field': 'id',
                    'required': True,
                    'type': 'integer',
                },
                {
                    'field': 'first_name',
                    'required': False,
                    'type': 'string',
                },
                {
                    'field': 'last_name',
                    'required': False,
                    'type': 'string',
                },
                {
                    'field': 'country',
                    'required': False,
                    'type': 'string'
                },
                {
                    'field': 'age',
                    'required': False,
                    'type': 'integer',
                },
                {
                    'field': 'type',
                    'required': False,
                    'type': 'integer',
                },
                {
                    'field': 'value',
                    'required': False,
                    'type': 'float',
                },
            ]
            ret = check_payloads(exp_args, payload)
            if ret == -1:
                return Response(RES_ERR_MISSING_FIELD, status=400)
            elif ret == -2:
                return Response(RES_ERR_INVALID_FILED, status=400)

            first_name = payload.get('first_name')
            last_name = payload.get('last_name')
            country = payload.get('country')
            age = payload.get('age')
            type = payload.get('type')
            value = payload.get('value')

            if (not first_name) and (not last_name) and (not country) and (not age) and (not type) and (not value):
                return Response(RES_ERR_MISSING_FIELD, status=400)

            if age:
                age = int(age)
                if age < 18 or age > 40:
                    return Response(RES_ERR_INVALID_FILED, status=400)

            if type:
                type = int(type)
                if type < 0 or type > 3:
                    return Response(RES_ERR_INVALID_FILED, status=400)

            if value:
                value = float(value)

            # if member does not exist
            member_id = int(payload.get('id'))
            if len(TBLMember.objects.filter(id=member_id)) == 0:
                return Response(RES_ERR_MEMBER_NOT_EXIST, status=400)

            # update member
            member = TBLMember.objects.get(id=member_id)
            if first_name:
                member.first_name = first_name
            if last_name:
                member.last_name = last_name
            if type:
                member.type = type
            if country:
                member.country = country
            if age:
                member.age = age
            if value:
                member.value = value

            member.save()

            return Response(RES_OK_MEMBER_UPDATED, status=200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)

    @administrator_func
    def delete(self, request):
        """Delete a member

        (This api is for administrator)

        Url
            /member/
        Method
            PUT
        Payload
            token (*)
            id (*)
                Id of member to be deleted
        Returns:
            Dictionary with code and message. Possible values are as following.
            - when success
                - RES_OK_MEMBER_DELETED         (HttpStatusCode = 204)
            - when fail
                - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                - RES_ERR_MISSING_FIELD         (HttpStatusCode = 400)
                - RES_ERR_INVALID_FILED         (HttpStatusCode = 400)
                - RES_ERR_MEMBER_NOT_EXIST      (HttpStatusCode = 400)
                - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            # check payload
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

            # if member does not exist
            member_id = int(payload.get('id'))
            if len(TBLMember.objects.filter(id=member_id)) == 0:
                return Response(RES_ERR_MEMBER_NOT_EXIST, status=400)

            # delete member
            member = TBLMember.objects.get(id=member_id)
            member.delete()

            return Response(RES_OK_MEMBER_DELETED, status=204)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)