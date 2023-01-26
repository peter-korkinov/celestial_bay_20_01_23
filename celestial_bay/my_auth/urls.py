from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView, UpdateUserView, ChangePasswordView, LogoutView,\
    UserView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(),
         name='auth_change_password'),
    path('update_user/<int:pk>/', UpdateUserView.as_view(), name='auth_update_user'),
    path('users/<uuid:pk>/', UserView.as_view(), name='auth_users'),
]
