# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# UserModel = get_user_model()

# class UserLoginSerializer(serializers.Serializer):
#     phone_number = serializers.CharField(max_length=15)
#     otp = serializers.CharField(max_length=6)
from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(required=False)
