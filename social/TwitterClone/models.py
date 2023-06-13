from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Meeps(models.Model):
    user = models.ForeignKey(
        User, related_name="meeps",
        on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=250)
    createdAt = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="meepLike", blank=True)


    def numberOfLikes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user} created at {self.createdAt:%Y-%m-%d %H:%M} {self.body}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                     related_name="followedBy", # Way to look up whos following you.
                                     symmetrical=False, # Means that both dont have to be true, so if I follow you, you dont have to follow me.
                                     blank=True) # Basically it can be null, you dont have to follow anyone.
    dateModified = models.DateTimeField(User, auto_now=True)
    profileImage = models.ImageField(null=True, blank=True, upload_to="images/")
    profileBio = models.CharField(null=True, blank=True, max_length=2000)
    
    def __str__(self):
        return self.user.username

    
# function to make the user a profile when they sign up.
@receiver(post_save, sender=User) # Decorator that calls this function whenever a new user is saved.
def createProfile(sender, instance , created, **Kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(createProfile, sender=User)