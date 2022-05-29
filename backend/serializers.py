from rest_framework import serializers
from .models import ProfileInfo, SocialAccount
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

# registration serializer...


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_fields = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        else:
            return('Invalid details')


# create serializers for my user linked models...


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileInfo
        fields = ('name', 'about', 'address')

    def create(self, validated_data):
        profile = ProfileInfo.objects.create(**validated_data)

        return profile

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.about = validated_data['about']
        instance.address = validated_data['address']
        instance.save()
        return instance


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ('type', 'handle', 'url')
