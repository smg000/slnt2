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
    url_root = models.URLField(max_length=500, default='', help_text='Add URL without trailing slash.')
    url_full = models.URLField(max_length=500, default='')
    url_keys_include = models.TextField(blank=True, help_text='Separate keywords with a comma, no space.')
    url_keys_exclude = models.TextField(default='somenonsensestring')
    url_prepend = models.URLField(max_length=500, blank=True, null=True, default='', help_text='Add URL without trailing slash.')
    scrape = models.BooleanField(default=False)
    def __str__(self):
        return "%s" % (self.publication_name)

class Article(models.Model):
    issue = models.ForeignKey(Issue, default=None, on_delete=models.PROTECT)
    publication_name = models.ForeignKey(Publication, blank=True, null=True, default='', on_delete=models.PROTECT)
    title = models.CharField(max_length=250)
    byline = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date(1900, 1, 1))
    url = models.URLField(max_length=250)
    text = models.TextField(blank=True)
    bias = models.IntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Select a number between 0 and 100, where 0 is extremely liberal, and 100 is extremely conservative.')
    display = models.BooleanField(default=False)
    def __str__(self):
        return "%s" % (self.title)

# OBSOLETE CLASS
class Site(models.Model):
    publication_name = models.CharField(max_length=250)
    url_root = models.URLField(max_length=500)
    url_full = models.URLField(max_length=500)
    url_keys_include = models.TextField(blank=True)
    url_keys_exclude = models.TextField()
    url_prepend = models.URLField(max_length=500, blank=True, null=True, default='')
    def __str__(self):
        return "%s" % (self.publication_name)