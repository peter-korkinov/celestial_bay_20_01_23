from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import RegisterSerializer, ChangePasswordSerializer,\
    UpdateUserSerializer


class RegisterView(generics.CreateAPIView):
    """
    For registering new users.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    For changing the password of an existing user.
    It requires user to be authenticated.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateUserView(generics.UpdateAPIView):
    """
    For updating user info.
    It requires user to be authenticated.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class LogoutView(APIView):
    """
    For logging out a user.
    It requires user to be authenticated.
    """

    permission_classes = (IsAuthenticated,)

    # Using the SimpleJWT library's token_blacklist app functionality for
    # blacklisting tokens.
    #
    # Simple JWT will add any generated refresh or sliding tokens to a list of
    # outstanding tokens. It will also check that any refresh or sliding token
    # does not appear in a blacklist of tokens before it considers it as valid.
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

