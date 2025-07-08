from rest_framework import serializers
from .models import Team, Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        exclude = ['team']  # 👈 We do not send team from frontend

class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'location', 'skill_level', 'manager', 'players']  # ✅ players included

    def create(self, validated_data):
        players_data = validated_data.pop('players')
        team = Team.objects.create(**validated_data)

        captain_count = 0
        for player_data in players_data:
            if player_data.get('is_captain'):
                captain_count += 1
            Player.objects.create(team=team, **player_data)

        if captain_count > 1:
            raise serializers.ValidationError("Only one captain is allowed per team.")

        return team
