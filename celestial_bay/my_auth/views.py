from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import RegisterSerializer, ChangePasswordSerializer, \
    UpdateUserSerializer, UserSerializer, CustomTokenObtainPairSerializer


class IsNotAuthenticated(BasePermission):
    """
    Allows access only to NOT authenticated users.
    """

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)


class IsOwnerOfObject(BasePermission):
    """
    The request is from the owner of the object, or is a read-only request.

    A custom permission class extending BasePermission.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class RegisterView(generics.CreateAPIView):
    """
    For registering new users.
    """
    queryset = User.objects.all()
    permission_classes = (IsNotAuthenticated,)
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns user info(id, first_name,
    last_name, email), an access and refresh JSON web token pair to prove
    the authentication of those credentials.
    """
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    For changing the password of an existing user.
    It requires user to be authenticated.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOfObject)
    serializer_class = ChangePasswordSerializer
    http_method_names = ['put']


class UpdateUserView(generics.UpdateAPIView):
    """
    For updating user info.
    It requires user to be authenticated.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
    http_method_names = ['put']


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


class UserView(generics.RetrieveAPIView):
    """
    For getting a user's info.

    It inherits from generics.RetrieveAPIView and supports GET queries only for
    single user by user id.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
