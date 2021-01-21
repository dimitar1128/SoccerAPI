from .base import *
from module.user import *

class Market(viewsets.ViewSet):

    @token_required
    def list(self, request):
        """List all members on the transfer list

        Url
            /market/
        Method
            GET
        Payload
            token (*)
            filter_country
            filter_team_name
            filter_player_name
            filter_value_lte
            filter_value_gte

        If any of filter_* values are not passed, it should return all members on the transfer list.
        Otherwise, return members who fit the filter criteria

        - when success
            Member list on the transfer list        (HttpStatusCode = 200)
        - when fail
            - RES_ERR_TOKEN_REQUIRED                (HttpStatusCode = 401)
            - RES_ERR_INVALID_TOKEN                 (HttpStatusCode = 401)
            - RES_ERR_INTERNAL_SERVER               (HttpStatusCode = 500)
        """
        try:
            payload = request.POST
            filter_country = payload.get('filter_country')
            filter_team_name = payload.get('filter_team_name')
            filter_player_name = payload.get('filter_player_name')
            filter_value_lte = payload.get('filter_value_lte')
            filter_value_gte = payload.get('filter_value_gte')

            if filter_value_gte:
                filter_value_gte = float(filter_value_gte)
            if filter_value_lte:
                filter_value_lte = float(filter_value_lte)

            all_markets = TBLMarket.objects.all()
            members = []

            team_dict = {}
            teams = list(TBLTeam.objects.all().values())
            for team in teams:
                team_dict[team['id']] = {
                    'name': team['name']
                }

            # iterate all members on the transfer list, check if they fit filter criteria
            for market in all_markets:
                member = market.member

                if filter_country and member.country != filter_country:
                    continue
                if filter_team_name and team_dict[member.team_id]['name'] != filter_team_name:
                    continue
                name = member.first_name + ' ' + member.last_name
                if filter_player_name and name != filter_player_name:
                    continue

                if filter_value_gte != None and market.price < filter_value_gte:
                    continue
                if filter_value_lte != None and market.price > filter_value_lte:
                    continue

                members.append({
                    'first_name': member.first_name,
                    'last_name': member.last_name,
                    'country': member.country,
                    'team_name': team_dict[member.team_id]['name'],
                    'value': member.value,
                    'price': market.price,
                })

            return Response(members, status=200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)


    @token_required
    def create(self, request):
        """Set a player on transfer list

        Url
            /market/
        Method
            POST
        Payload
            token (*)
            member_id (*)
            price (*)

        Returns:
            Dictionary with code and message. Possible values are as following.
                - when success
                    - RES_OK_SET_ON_TRANSFER_LIST   (HttpStatusCode = 201)
                - when fail
                    - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                    - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                    - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                    - RES_ERR_MISSING_FIELD         (HttpStatusCode = 400)
                    - RES_ERR_ALREADY_ON_MARKET     (HttpStatusCode = 400)
                    - RES_ERR_INVALID_PRICE         (HttpStatusCode = 400)
                    - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            # parameter check
            payload = self.request.POST
            exp_args = [
                'member_id',
                'price',
            ]
            if not check_arguments(exp_args, payload):
                return Response(RES_ERR_MISSING_FIELD, status=400)

            member_id = int(payload['member_id'])
            price = float(payload['price'])

            if price <= 0:
                return Response(RES_ERR_INVALID_PRICE, status=400)

            user = get_user_with_token(
                payload['token']
            )
            if not user:
                return Response(RES_ERR_INTERNAL_SERVER, status=500)

            team_obj = TBLTeam.objects.get(owner_id=user.id)

            # if the user is not administrator, and the member is not the user's team member
            if user.is_superuser == 0 and len(team_obj.members.filter(id=member_id)) == 0:
                return Response(RES_ERR_INVALID_PERMISSION, status=401)

            # if the user is already on the transfer list
            if len(TBLMarket.objects.filter(member_id=member_id)) > 0:
                return Response(RES_ERR_ALREADY_ON_MARKET, status=400)

            obj = TBLMarket()
            obj.member_id = member_id
            obj.price = price
            obj.save()

            return Response(RES_OK_SET_ON_TRANSFER_LIST, status=201)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)


    @token_required
    def put(self, request):
        """Buy a player of transfer list

        Url
            /market/
        Method
            PUT
        Payload
            token (*)
            member_id (*)

        Returns:
            Dictionary with code and message. Possible values are as following.
                - when success
                    - RES_OK_BUY_PLAYER                     (HttpStatusCode = 200)
                - when fail
                    - RES_ERR_TOKEN_REQUIRED                (HttpStatusCode = 401)
                    - RES_ERR_INVALID_TOKEN                 (HttpStatusCode = 401)
                    - RES_ERR_MISSING_FIELD                 (HttpStatusCode = 400)
                    - RES_ERR_MEMBER_NOT_ON_MARKET          (HttpStatusCode = 400)
                    - RES_ERR_NOT_ALLOW_TO_BUY_OWN_PLAYER   (HttpStatusCode = 400)
                    - RES_ERR_NOT_ENOUGH_MONEY_TO_BUY       (HttpStatusCode = 400)
                    - RES_ERR_INTERNAL_SERVER               (HttpStatusCode = 500)
        """
        try:
            # parameter check
            payload = request.POST
            member_id = payload.get('member_id')
            if not member_id:
                return Response(RES_ERR_MISSING_FIELD, status=400)

            user = get_user_with_token(
                payload['token']
            )
            if not user:
                return Response(RES_ERR_INTERNAL_SERVER, status=500)

            # if the member is not on the transfer list
            if len(TBLMarket.objects.filter(member_id=member_id)) == 0:
                return Response(RES_ERR_MEMBER_NOT_ON_MARKET, status=400)

            # if the member is the requestor's team member
            team = TBLTeam.objects.get(owner_id=user.id)
            if len(team.members.filter(id=member_id)) > 0:
                return Response(RES_ERR_NOT_ALLOW_TO_BUY_OWN_PLAYER, status=400)

            # if team's extra money is less than the member's market value
            market = TBLMarket.objects.get(member_id=member_id)
            if team.extra_value < market.price:
                return Response(RES_ERR_NOT_ENOUGH_MONEY_TO_BUY, status=400)

            # remove member from original team, update the original team's extra value
            member = TBLMember.objects.get(id=member_id)
            orig_team = TBLTeam.objects.get(id=market.member.team_id)
            orig_team.members.remove(member)
            orig_team.extra_value += market.price
            orig_team.save()

            # add member to the new team, update team's extra value
            team.members.add(member)
            team.extra_value -= market.price
            team.save()

            # update the member's value, team id
            member.value += member.value * (random.randint(10, 100) / 100)
            member.team_id = team.id
            member.save()

            # delete member from market
            market.delete()

            return Response(RES_OK_BUY_PLAYER, status=200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)