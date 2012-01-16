from django.db import models
from django.contrib.auth.models import User

class Keyword(models.Model):
    keyword_str = models.CharField(max_length=40)
    def __unicode__(self):
        return self.keyword_str

class User_Profile(models.Model):
    user        = models.ForeignKey(User, unique=True)
    keywords    = models.ManyToManyField(Keyword, null=True, blank=True)

class Video_Profile(models.Model):
    video_url   = models.URLField()
    keywords    = models.ManyToManyField(Keyword, null=True, blank=True)
