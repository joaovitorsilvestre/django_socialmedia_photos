import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

def user_path(instance, filename):
    return ('users/{}/{}'.format(instance.username, filename))

class RequestsFriends(models.Model):
    user_that_request = models.CharField(max_length=50)

    def __str__(self):
        return self.user_that_request

class Usuario(AbstractUser):
    activation_key = models.CharField(max_length=30)
    friends = models.ManyToManyField('self', blank=True)
    request_friends = models.ManyToManyField(RequestsFriends, blank=True)
    images = models.FileField(null=True, blank=True, upload_to=user_path)

    def get_images(self):
        basedir = settings.BASE_DIR
        path = basedir + "/media/users/{}".format(self.username)
        print(path)

        images = []
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                images.append(name)

        return images
