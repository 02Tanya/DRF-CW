from users.models import User
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):

    def create(self, validate_data):
        user = User.objects.create(email=validate_data['email'],)
        user.set_password(validate_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'password',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'email', 'avatar', 'telegram_chat_id')
