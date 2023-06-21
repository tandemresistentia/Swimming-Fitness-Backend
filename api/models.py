from django.db import models
from accounts.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE ,default='None')
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, default='??')
    location = models.CharField(max_length=100, default='??')
    total_distance_swum = models.FloatField(default=0)
    average_lap_time = models.FloatField(default=0)
    completed_challenges = models.IntegerField(default=0)

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class LogTraining(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    distance = models.FloatField(max_length=100)
    time = models.FloatField(max_length=100)
    fastest_lap = models.FloatField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"LogTraining {self.id}"
    

class Challenge(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    challenge_type = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=20,default='pending')
    

    # Add any additional fields as per your requirements

    def __str__(self):
        return self.challenge_type
    

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name