from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    rating = models.IntegerField(default=1200)
    problems_solved = models.IntegerField(default=0)
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_rank(self):
        if self.rating >= 2400:
            return "Grandmaster"
        elif self.rating >= 2100:
            return "Master"
        elif self.rating >= 1900:
            return "Expert"
        elif self.rating >= 1600:
            return "Specialist"
        elif self.rating >= 1400:
            return "Pupil"
        else:
            return "Newbie"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
