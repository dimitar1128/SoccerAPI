from .base import *
from module.team import *
from module.user import *

class TeamOwner(viewsets.ViewSet):
    @token_required
    def list(self, request):
        """Get owner team information

        Url
            /team/my_team
        Method
            GET
        Payload
            token

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
                return Response(RES_ERR_INTERNAL_SERVER, 500)

            team_obj = TBLTeam.objects.get(owner_id = user.id)
            team = get_team_by_id(team_obj.id)
            if not team:
                return Response(RES_ERR_INTERNAL_SERVER, 500)

            return Response(team, 200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, 500)

