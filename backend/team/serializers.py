from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team

User = get_user_model()

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'role')

class TeamListSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'owner','members', 'created_at']

class TeamDetailSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer(read_only=True)
    members = UserSimpleSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True, source='members'
    )

    class Meta:
        model = Team
        fields = ['id', 'name', 'owner', 'members', 'member_ids', 'created_at']

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        # validated_data içinden owner varsa çıkar
        owner = self.context['request'].user
        validated_data.pop('owner', None)  # <-- eklendi!
        # Owner'ı daima üyeler listesine ekle
        if owner not in members:
            members.append(owner)
        team = Team.objects.create(owner=owner, **validated_data)
        team.members.set(members)
        return team

    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        owner = instance.owner
        if members is not None:
            # Owner daima üyeler arasında olsun
            if owner not in members:
                members.append(owner)
            instance.members.set(members)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
