from rest_framework import serializers
from .models import Profile,Challenge,LogTraining

from accounts.models import CustomUser
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Profile
        fields = '__all__'

    def update(self, instance, validated_data):
        # Handle the update logic for your dotted-source fields
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.location = validated_data.get('location', instance.location)
        instance.completed_challenges = validated_data.get('completed_challenges', instance.completed_challenges)
        instance.total_distance_swum = validated_data.get('total_distance_swum', instance.total_distance_swum)
        instance.average_lap_time = validated_data.get('average_lap_time', instance.average_lap_time)
        # Update other fields as needed
        username = validated_data.get('user', instance.user.username)
        username = username.get('username')
        instance.user.username = username
        instance.user.save()
        instance.save()
        return instance

class LogTrainingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = LogTraining
        fields = ['username', 'distance', 'time', 'fastest_lap']

class ChallengeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Challenge
        fields = ['id','challenge_type', 'description', 'status', 'username']