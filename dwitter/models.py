from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    follows = models.ManyToManyField(
        "self",
        related_name = "followed_by",
        symmetrical = False,
        blank = True,
    )

    def __str__(self):
        return self.user.username

class Dweet(models.Model):
    user = models.ForeignKey(
        User,
        related_name = "dweets",
        on_delete = models.DO_NOTHING,
    )
    body = models.CharField(max_length = 512)
    liked_by = models.ManyToManyField(
        User,
        related_name = "liked",
        blank = True
    )
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}"
        )
    
@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs): #sender is redundant. it's not being used in this case. used in multi models
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()