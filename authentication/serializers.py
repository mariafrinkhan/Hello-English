from .models import *
from djoser.serializers import *

# class CustomUserCreateSerializer(UserCreateSerializer):
#     class Meta(UserCreateSerializer.Meta):
#         model = CustomUser
#         fields = ['id', 'email', 'first_name', 'last_name', 'password']

# class CustomUserSerializer(UserSerializer):
#     class Meta(UserSerializer.Meta):
#         model = CustomUser
#         fields = ['id', 'email', 'first_name', 'last_name']


class UserCreateSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 're_password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')
        role = validated_data.pop('role', 'user')

        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=role
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'role')


