from django.db import models
from django.contrib.auth.models import User
import conf

class Keyword(models.Model):
    keyword = models.CharField(max_length=200)
    def __unicode__(self):
        return self.keyword

class Profile(models.Model):
    user        = models.OneToOneField(User)
    language    = models.CharField(max_length=2, choices=conf.LANGUAGES)
    keywords    = models.ManyToManyField(Keyword, null=True, blank=True)
    def __unicode__(self):
        return self.user.username

class Institution(models.Model):
    name    = models.CharField(max_length=500)
    link    = models.URLField(max_length=500)
    rss     = models.URLField(max_length=500)
    def __unicode__(self):
        return self.name

class Course(models.Model):
    title       = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    url         = models.URLField(max_length=500)
    keywords    = models.ManyToManyField(Keyword, null=True, blank=True)
    lecturer    = models.CharField(max_length=500)
    institution = models.ForeignKey(Institution)
    def __unicode__(self):
        return self.title

class Lecture(models.Model):
    number      = models.IntegerField()
    title       = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    url         = models.URLField(max_length=500, blank=True, null=True)
    video       = models.URLField(max_length=500, blank=True, null=True)
    lecturer    = models.CharField(max_length=500)
    course      = models.ForeignKey(Course, related_name='course')
    def __unicode__(self):
        return self.title

class Note(models.Model):
    text    = models.TextField(null=True, blank=True)
    user    = models.ForeignKey(User)
    lecture = models.ForeignKey(Lecture)

class Question(models.Model):
    text        = models.CharField(max_length=500)
    user        = models.ForeignKey(User, unique=True)
    lecture     = models.ForeignKey(Lecture, unique=True)
    date        = models.DateTimeField(auto_now=True)
    up_votes    = models.IntegerField()
    down_votes  = models.IntegerField()

class Answer(models.Model):
    text        = models.CharField(max_length=500)
    user        = models.ForeignKey(User, unique=True)
    question    = models.ForeignKey(Question, unique=True)
    date        = models.DateTimeField(auto_now=True)
    up_votes    = models.IntegerField()
    down_votes  = models.IntegerField()
