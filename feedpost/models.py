from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from datetime import datetime
from django.dispatch import receiver


class CustomUser(AbstractUser):
    is_parent = models.BooleanField(default=True)
    is_guest = models.BooleanField(default=False)

    def add_user(self):
        return self.save()
    

    def get_absolute_url(self):
        if self.is_parent:
            return reverse('parent')    
        else: 
            return reverse('guest')


class ParentProfile(models.Model):
    parent_name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_image = CloudinaryField('image', default='placeholder')

    def get_absolute_url(self):
        return reverse('add_child')

    def __str__(self):
        return self.parent_name
     

class GuestProfile(models.Model):
    guest_name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile_image = CloudinaryField('image', default='placeholder') 
    

    def get_absolute_url(self):
        return reverse('profile')

    def __str__(self):
        return self.guest_name    


class Profile(models.Model):
    child_name = models.CharField(max_length=200, unique=True) 
    id_child = models.IntegerField(default=None)
    user = models.ForeignKey(ParentProfile, on_delete=models.CASCADE)
    profile_image = CloudinaryField('image', default='placeholder') 
    birthdate = models.DateField()
    friends = models.ManyToManyField(CustomUser, related_name='friends', blank=True)
    
    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()    

    def get_absolute_url(self):
        return reverse('profile')

    def __str__(self):
        return self.child_name

STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name = 'sender')
    receiver = models.ForeignKey(GuestProfile, on_delete=models.CASCADE, related_name = 'receiver')
    status = models.CharField (max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True) 
    #profile = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="child_profile")
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    media = CloudinaryField('media', default='placeholder')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    likes = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes', default=None)

    class Meta:
        verbose_name_plural = "Posts"
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()   

    def get_absolute_url(self):
        return reverse('profile')


class Comment(models.Model):
    name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now_add=True)
    deleted_on = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['created_on']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)     
    
    def __str__(self):
        return '%s - %s' %(self.post.title, self.name)

