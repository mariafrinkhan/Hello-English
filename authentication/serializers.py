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
        fields = ('id','first_name', 'last_name', 'username', 'email', 'password', 're_password', 'role',"mobile")
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')
        role = validated_data.pop('role', 'user')
        mobile = validated_data.pop('mobile', None)

        return User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            username=validated_data.get('username'),
            email=validated_data['email'],
            password=validated_data['password'],
            role=role,
            mobile=mobile
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'username', 'email', 'role',"mobile")


