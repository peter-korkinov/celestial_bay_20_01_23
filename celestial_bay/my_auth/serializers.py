from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    For registering of new users using the custom user model.

    email, password, password2, first_name, last_name are required fields.
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        """
        Validates if the two password fields match.
        """

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields do not match'}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extends the SimpleJWT's TokenObtainPairSerializer by adding user info(id,
    first_name, last_name, email), beside the access and refresh tokens, to  the
    response.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
        }
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    For changing the password of an existing user.

    old_password, password, password2 are required fields.
    """

    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        """
        Validates if the password and password2 fields match
        """

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields do not match.'}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")

        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {'authorization': 'You do not have permission for this user.'}
            )

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    """
    For updating the info of a user.

    Fields able to be updated: email, first_name, last_name.
    """

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        """
        Validates if the new email provided is not already in use.
        """

        user = self.context['request'].user

        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError('This email is already in use.')

        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {'authorization': 'You do not have permission for this user.'}
            )

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']

        instance.save()

        return instance


class UserSerializer(FlexFieldsModelSerializer):
    """
    For retrieving the user info.

    It inherits from the DRF-FlexFields' FlexFieldsModelSerializer

    fields: pk, first_name, last_name, date_joined, last_login
    expandable fields: galaxies
    """

    class Meta:
        model = User
        fields = ['pk', 'first_name', 'last_name', 'date_joined', 'last_login']
        expandable_fields = {
            'galaxies': ('galaxies.GalaxySerializer', {'many': True})
        }
