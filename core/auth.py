from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from ninja.security import HttpBearer


class KnoxAuth(HttpBearer):
    def authenticate(self, request, token):
        knox_auth = KnoxTokenAuthentication()
        try:
            user_auth_tuple = knox_auth.authenticate_credentials(token.encode("utf-8"))
        except:
            return

        if user_auth_tuple is not None:
            return user_auth_tuple[0]
