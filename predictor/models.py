from django.db import models
from django.contrib.auth.models import User


class PredictionHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    hours = models.FloatField()

    result = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to="profile_pics/",
        default="default.png"
    )

    def __str__(self):
        return self.user.username