from .base import *
from django.contrib.auth import authenticate


class Login(viewsets.ViewSet):
    def create(self, request):
        """Login user

        Check user account, login user and generate a token that should be used for further api requests

        Url
            /auth/login/
        Method
            POST
        Payload
            email (*)
            password (*)

        Returns:
            - when success
                Dictionary with token and expires_at time. (HttpStatusCode = 200)
            - when fail
                Dictionary with code and message. Possible values are as following.
                    - RES_ERR_MISSING_FIELD         (HttpStatusCode = 400)
                    - RES_ERR_INVALID_CREDENTIAL    (HttpStatusCode = 400)
                    - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            payload = self.request.POST
            exp_args = [
                'email',
                'password'
            ]
            if not check_arguments(exp_args, payload):
                return Response(RES_ERR_MISSING_FIELD, status=400)

            user = authenticate(
                username=payload['email'],
                password=payload['password'],
            )
            if not user:
                return Response(RES_ERR_INVALID_CREDENTIAL, status=400)

            token = generate_token()
            # regenerate token if it is already registered
            while len(list(TBLToken.objects.filter(token=token))) > 0:
                token = generate_token()

            # save token
            token_obj = TBLToken()
            token_obj.token = token
            token_obj.user_id = user.id
            token_obj.save()

            expires_at = token_obj.created_time + datetime.timedelta(seconds=TOKEN_LIFE_TIME)

            return Response({
                'token': token,
                'expires_at': expires_at.strftime('%Y-%m-%d %H:%M:%S GMT+0')
            }, 200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)