from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance:User, created:bool, **kwargs) -> None:
    '''
    Automatically create a profile whenever a new user is created.
    '''
    if created:
        Profile.objects.create(user=instance)