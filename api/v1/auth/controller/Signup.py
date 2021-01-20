from .base import *
from module.team import *

class Signup(viewsets.ViewSet):

    def create(self, request):
        """Sign up user

        Url
            /auth/signup/
        Method
            POST
        Payload
            email
            password

        Returns:
              Dictionary with code and message. Possible values are as following.
                - RES_OK_USER_CREATED       (HttpStatusCode = 201)
                - RES_ERR_USER_EXIST        (HttpStatusCode = 409)
                - RES_ERR_MISSING_FIELD     (HttpStatusCode = 400)
                - RES_ERR_TEAM_CREATE       (HttpStatusCode = 500)
                - RES_ERR_INTERNAL_SERVER   (HttpStatusCode = 500)
        """
        try:
            exp_args = [
                'email',
                'password'
            ]
            payload = request.POST
            if not check_arguments(exp_args, payload):
                return Response(RES_ERR_MISSING_FIELD, 400)

            if len(list(TBLUser.objects.filter(email=payload['email']))) > 0:
                return Response(RES_ERR_USER_EXIST, 409)

            user = TBLUser()
            user.username = payload['email']
            user.email = payload['email']
            user.set_password(payload['password'])
            user.save()

            ret = create_team(user.id)
            # if team create is failed, remove registered user
            if not ret:
                user.delete()
                return Response(RES_ERR_TEAM_CREATE, 500)

            return Response(RES_OK_USER_CREATED, 201)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, 500)
