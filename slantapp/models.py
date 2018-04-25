from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime

class Issue(models.Model):
    issue = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date(1900, 1, 1))
    display = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    # Add include/do not include field
    def __str__(self):
        return "%s" % (self.issue)

class Publication(models.Model):
    publication_name = models.CharField(max_length=250)
    publication_logo = models.ImageField()
    # Add include/do not include field
    def __str__(self):
        return "%s" % (self.publication_name)

class Article(models.Model):
    issue = models.ForeignKey(Issue, default=None, on_delete=models.PROTECT)
    publication_name = models.ForeignKey(Publication, blank=True, null=True, default='', on_delete=models.PROTECT)
    title = models.CharField(max_length=250)
    byline = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date(1900, 1, 1))
    url = models.URLField(max_length=250)
    bias = models.IntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)])
    display = models.BooleanField(default=False)
    # Add include/do not include field
    def __str__(self):
        return "%s" % (self.title)

class Site(models.Model):
    publication_name = models.CharField(max_length=250)
    url_root = models.URLField(max_length=500)
    url_full = models.URLField(max_length=500)
    url_keys_include = models.TextField()
    url_keys_exclude = models.TextField()
    def __str__(self):
        return "%s" % (self.title)