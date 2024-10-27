from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model

class Idea(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)  # Consider using a specialized PhoneField if necessary
    email = models.EmailField()
    occupation = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=500)
    sdg_goal = models.CharField(max_length=50)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.description[:30]}" if self.description else self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=50,
        choices=[('student', 'Student'), ('mentor', 'Mentor'), ('organization', 'Organization')]
    )
    interests = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class IndividualProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()  # Changed to PositiveIntegerField to prevent negative ages
    occupation = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Individual Profile"

class BusinessProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_info = models.EmailField(max_length=100)  # Changed to EmailField

    def __str__(self):
        return f"{self.user.username}'s Business Profile"
