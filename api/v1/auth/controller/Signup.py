from .base import *
from module.team import *

class Signup(viewsets.ViewSet):

    def create(self, request):
        """Sign up user

        Url
            /signup/
        Method
            POST
        Payload
            email (*)
            password (*)

        Returns:
              Dictionary with code and message. Possible values are as following.
                - RES_OK_USER_CREATED       (HttpStatusCode = 201)
                - RES_ERR_USER_EXIST        (HttpStatusCode = 409)
                - RES_ERR_MISSING_FIELD     (HttpStatusCode = 400)
                - RES_ERR_INVALID_FILED         (HttpStatusCode = 400)
                - RES_ERR_TEAM_CREATE       (HttpStatusCode = 500)
                - RES_ERR_INTERNAL_SERVER   (HttpStatusCode = 500)
        """
        try:
            # payload check
            payload = self.request.POST
            exp_args = [
                {
                    'field': 'email',
                    'required': True,
                    'type': 'string',
                },
                {
                    'field': 'password',
                    'required': True,
                    'type': 'string',
                }
            ]
            ret = check_payloads(exp_args, payload)
            if ret == -1:
                return Response(RES_ERR_MISSING_FIELD, status=400)
            elif ret == -2:
                return Response(RES_ERR_INVALID_FILED, status=400)

            if len(list(TBLUser.objects.filter(email=payload['email']))) > 0:
                return Response(RES_ERR_USER_EXIST, status=409)

            user = TBLUser()
            user.username = payload['email']
            user.email = payload['email']
            user.set_password(payload['password'])
            user.s_password = encode_password(payload['password'])
            user.save()

            ret = create_team(user.id)
            # if team create is failed, remove registered user
            if not ret:
                user.delete()
                return Response(RES_ERR_TEAM_CREATE, status=500)

            return Response(RES_OK_USER_CREATED, status=201)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)
