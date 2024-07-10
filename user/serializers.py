from rest_framework import serializers
from .models import Member, FamilyMember, User

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(required=False)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'image']

class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = '_all_'

class CreateFamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = [
            'full_name',
            'date_of_birth',
            'gender',
            'phone_number',
            'family_relation',
        ]

class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    family_members = FamilyMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = '_all_'

class MemberCreateUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    family_members = CreateFamilyMemberSerializer(many=True, required=False)
    gender = serializers.CharField(required=False)
    society = serializers.PrimaryKeyRelatedField(queryset=Member.objects.all(), required=False)

    class Meta:
        model = Member
        fields = '_all_'
    
    def create(self, validated_data):
        family_members_data = validated_data.pop('family_members', [])
        member = Member.objects.create(**validated_data)
        for family_member_data in family_members_data:
            FamilyMember.objects.create(member=member, **family_member_data)
        return member

    def update(self, instance, validated_data):
        family_members_data = validated_data.pop('family_members', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for family_member_data in family_members_data:
            family_member_id = family_member_data.get('id')
            if family_member_id:
                family_member = FamilyMember.objects.get(id=family_member_id, member=instance)
                for attr, value in family_member_data.items():
                    setattr(family_member, attr, value)
                family_member.save()
            else:
                FamilyMember.objects.create(member=instance, **family_member_data)

        return instance