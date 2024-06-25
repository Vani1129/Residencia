# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# UserModel = get_user_model()

# class UserLoginSerializer(serializers.Serializer):
#     phone_number = serializers.CharField(max_length=15)
#     otp = serializers.CharField(max_length=6)
from rest_framework import serializers
from .models import Member, FamilyMember
from django.contrib.auth.models import User


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(required=False)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = '__all__'
        
class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    family_members = FamilyMemberSerializer(many=True)
    class Meta:
        model = Member
        fields = '__all__'

