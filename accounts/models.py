from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

class Profile(models.Model):
    '''
    User profile model extending Django's built-in User.
    Stores additional user information and social links.
    '''
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name='User'
    )

    bio = models.TextField(blank=True, null=True, verbose_name='Biography')
    github_url = models.URLField(blank=True, null=True, verbose_name='GitHub Profile')
    linkedin_url = models.URLField(blank=True, null=True, verbose_name='LinkedIn Profile')
    avatar = models.ImageField(
        default="media/avatar.jpg",
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name='Profile Picture'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At') 

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = "Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def full_name(self):
        '''Return user's full name or username if not set.'''
        return self.user.get_full_name() or self.user.username

