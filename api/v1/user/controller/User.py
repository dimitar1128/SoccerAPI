from .base import *
from module.team import *

class User(viewsets.ViewSet):
    @administrator_func
    def list(self, request):
        """List all users

        (This api is for administrator)

        Url
            /user/
        Method
            GET
        Payload
            token (*)

        Returns:
            - when success
                List of dictionary of user's data (HttpStatusCode = 200)
            - when fail
                Dictionary with code and message. Possible values are as following.
                    - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                    - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                    - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                    - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            res = []
            users = list(TBLUser.objects.all())
            for user in users:
                if user.is_superuser == 1:
                    continue
                res.append({
                    'id': user.id,
                    'email': user.email,
                    'password': decode_password(user.s_password),
                })

            return Response(res, status=200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)


    @administrator_func
    def create(self, request):
        """Create an user

        Create an user, and his team.

        Url
            /user/
        Method
            POST
        Payload
            email (*)
                New user's email
            password (*)
                New user's password

        Returns:
            Dictionary with code and message. Possible values are as following.
                - when success
                    - RES_OK_USER_CREATED           (HttpStatusCode = 201)
                - when fail
                    - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                    - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                    - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                    - RES_ERR_MISSING_FIELD         (HttpStatusCode = 400)
                    - RES_ERR_INVALID_FILED         (HttpStatusCode = 400)
                    - RES_ERR_USER_EXIST            (HttpStatusCode = 409)
                    - RES_ERR_TEAM_CREATE           (HttpStatusCode = 500)
                    - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            # payload check
            payload = request.POST
            exp_args = [
                {
                    'field': 'email',
                    'required': True,
                    'type': 'string'
                },
                {
                    'field': 'password',
                    'required': True,
                    'type': 'string'
                },
            ]
            ret = check_payloads(exp_args, payload)
            if ret == -1:
                return Response(RES_ERR_MISSING_FIELD, status=400)
            elif ret == -2:
                return Response(RES_ERR_INVALID_FILED, status=400)

            # if user is already exist
            if len(TBLUser.objects.filter(email=payload['email'])) > 0:
                return Response(RES_ERR_USER_EXIST, status=409)

            # create user
            user = TBLUser()
            user.username = payload['email']
            user.email = payload['email']
            user.set_password(payload['password'])
            user.s_password = encode_password(payload['password'])
            user.save()

            # create a team for the user
            team_id = create_team(user.id)

            # if team create is failed, remove registered user
            if not team_id:
                user.delete()
                return Response(RES_ERR_TEAM_CREATE, status=500)

            return Response(RES_OK_USER_CREATED, status=201)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)


    @administrator_func
    def put(self, request):
        """Update an user (actually updates a password of user)

        (This api is for administrator)

        Url
            /user/
        Method
            PUT
        Payload
            token (*)
            email (*)
                user's email to be updated
            password (*)

        Returns:
            Dictionary with code and message. Possible values are as following.
                - when success
                    - RES_OK_USER_UPDATED           (HttpStatusCode = 200)
                - when fail
                    - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                    - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                    - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                    - RES_ERR_MISSING_FIELD         (HttpStatusCode = 400)
                    - RES_ERR_INVALID_FILED         (HttpStatusCode = 400)
                    - RES_ERR_USER_NOT_EXIST        (HttpStatusCode = 400)
                    - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            # payload check
            payload = request.POST
            exp_args = [
                {
                    'field': 'email',
                    'required': True,
                    'type': 'string'
                },
                {
                    'field': 'password',
                    'required': True,
                    'type': 'string'
                },
            ]
            ret = check_payloads(exp_args, payload)
            if ret == -1:
                return Response(RES_ERR_MISSING_FIELD, status=400)
            elif ret == -2:
                return Response(RES_ERR_INVALID_FILED, status=400)

            # if user is not exist
            if len(TBLUser.objects.filter(email=payload['email'])) == 0:
                return Response(RES_ERR_USER_NOT_EXIST, status=400)

            email = payload['email']
            password = payload['password']

            # update user's  password
            user = TBLUser.objects.get(email=email)
            user.set_password(password)
            user.s_password = encode_password(password)
            user.save()

            return Response(RES_OK_USER_UPDATED, status=200)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)


    @administrator_func
    def delete(self, request):
        """Delete an user

        (This api is for administrator)

        Url
            /user/
        Method
            DELETE
        Payload
            token (*)
            email (*)
                user's email to be deleted

        Returns:
            Dictionary with code and message. Possible values are as following.
                - when success
                    - RES_OK_USER_DELETED           (HttpStatusCode = 204)
                - when fail
                    - RES_ERR_TOKEN_REQUIRED        (HttpStatusCode = 401)
                    - RES_ERR_INVALID_TOKEN         (HttpStatusCode = 401)
                    - RES_ERR_INVALID_PERMISSION    (HttpStatusCode = 401)
                    - RES_ERR_MISSING_FIELD         (HttpStatusCode = 400)
                    - RES_ERR_INVALID_FILED         (HttpStatusCode = 400)
                    - RES_ERR_USER_NOT_EXIST        (HttpStatusCode = 400)
                    - RES_ERR_INTERNAL_SERVER       (HttpStatusCode = 500)
        """
        try:
            # payload check
            payload = request.POST
            exp_args = [
                {
                    'field': 'email',
                    'required': True,
                    'type': 'string'
                },
            ]
            ret = check_payloads(exp_args, payload)
            if ret == -1:
                return Response(RES_ERR_MISSING_FIELD, status=400)
            elif ret == -2:
                return Response(RES_ERR_INVALID_FILED, status=400)

            # if user is not exist
            if len(TBLUser.objects.filter(email=payload['email'])) == 0:
                return Response(RES_ERR_USER_NOT_EXIST, status=400)

            email = payload['email']
            user = TBLUser.objects.get(email=email)

            # delete all team members
            team = TBLTeam.objects.get(owner_id=user.id)
            members = list(team.members.all())
            for member in members:
                member.delete()

            # delete user
            user.delete()

            return Response(RES_OK_USER_DELETED, status=204)

        except Exception as e:
            logging.error(str(e))
            return Response(RES_ERR_INTERNAL_SERVER, status=500)
