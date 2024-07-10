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
        fields = ['id','email']

class FamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = '__all__'



class CreateFamilyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMember
        fields = [
            'fullname',
            'date_of_birth',
            'gender',
            'phone_number',
        ]


class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    family_members = FamilyMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Member
        fields = '__all__'
        
    # def to_represent(self, instance):
    #     return super().to_rese

        
class MemberCreateUpdateSerializer(serializers.ModelSerializer):
    family_members = CreateFamilyMemberSerializer(many=True, required=False)

    class Meta:
        model = Member
        fields = '__all__'
    
    def create(self, validated_data):
        family_members_data = validated_data.pop('family_members', [])

        print(family_members_data)
        member = Member.objects.create(**validated_data)
        for family_member_data in family_members_data:
            FamilyMember.objects.create(member=member, **family_member_data)
        return member

    def update(self, instance, validated_data):
        family_members_data = validated_data.pop('family_members', [])
        instance.society = validated_data.get('society', instance.society)
        instance.building = validated_data.get('building', instance.building)
        instance.flat_number = validated_data.get('flat_number', instance.flat_number)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.country = validated_data.get('country', instance.country)
        instance.member_type = validated_data.get('member_type', instance.member_type)
        instance.save()

        for family_member_data in family_members_data:
            family_member_id = family_member_data.get('id')
            if family_member_id:
                family_member = FamilyMember.objects.get(id=family_member_id, member=instance)
                family_member.fullname = family_member_data.get('fullname', family_member.fullname)
                family_member.date_of_birth = family_member_data.get('date_of_birth', family_member.date_of_birth)
                family_member.gender = family_member_data.get('gender', family_member.gender)
                family_member.phone_number = family_member_data.get('phone_number', family_member.phone_number)
                family_member.family_relation = family_member_data.get('family_relation', family_member.family_relation)
                family_member.save()
            else:
                FamilyMember.objects.create(member=instance, **family_member_data)

        return instance
 