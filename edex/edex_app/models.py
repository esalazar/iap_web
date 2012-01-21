from django.db import models
from django.contrib.auth.models import User

LANGUAGES = (
    ('English', 'en'),
    ('Spanish', 'es'),
)

class Keyword(models.Model):
    keyword_str = models.CharField(max_length=40)

class Profile(models.Model):
    user        = models.ForeignKey(User, unique=True)
    language    = models.CharField(max_length=2, choices=LANGUAGES)
    keywords    = models.ManyToManyField(Keyword, null=True, blank=True)

class Institution(models.Model):
    name    = models.CharField(max_length=100)
    link    = models.URLField()
    rss     = models.URLField()

class Class(models.Model):
    title       = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    url         = models.URLField()
    keywords    = models.ManyToManyField(Keyword, null=True, blank=True)
    lecturer    = models.CharField(max_length=100)
    institution = models.ForeignKey(Institution)

class Lecture(models.Model):
    title       = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    url         = models.URLField(blank=True, null=True)
    video       = models.URLField(blank=True, null=True)
    lecturer    = models.CharField(max_length=100)
    lec_class   = models.ForeignKey(Class, related_name='class')

class Note(models.Model):
    text    = models.TextField(null=True, blank=True)
    user    = models.ForeignKey(User, unique=True)
    lecture = models.ForeignKey(Lecture, unique=True)

class Question(models.Model):
    text        = models.CharField(max_length=200)
    user        = models.ForeignKey(User, unique=True)
    lecture     = models.ForeignKey(Lecture, unique=True)
    date        = models.DateTimeField(auto_now=True)
    up_votes    = models.IntegerField()
    down_votes  = models.IntegerField()

class Answer(models.Model):
    text        = models.CharField(max_length=200)
    user        = models.ForeignKey(User, unique=True)
    question    = models.ForeignKey(Question, unique=True)
    date        = models.DateTimeField(auto_now=True)
    up_votes    = models.IntegerField()
    down_votes  = models.IntegerField()
