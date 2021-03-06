from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django import utils
import datetime

class Issue(models.Model):
    issue = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date(1900, 1, 1))
    summary_main = models.TextField(blank=True, null=True, default='', help_text='Add short summary of the topic.')
    summary_left = models.TextField(blank=True, null=True, default='', help_text='Add summary of the left.')
    summary_right = models.TextField(blank=True, null=True, default='', help_text='Add summary of the right.')
    stage = models.BooleanField(default=False)
    display = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    weekend_order = models.IntegerField(default=0)
    def __str__(self):
        # return "%s:\t %s" % (self.id, self.issue)
        return self.issue

class Publication(models.Model):
    publication_name = models.CharField(max_length=250)
    publication_logo = models.ImageField()
    url_root = models.URLField(max_length=500, default='', help_text='Add URL without trailing slash.')
    url_full = models.URLField(max_length=500, default='')
    regex = models.TextField(blank=True, null=True)
    url_blacklist = models.TextField(blank=True, null=True, default='')
    prepend = models.BooleanField(default=False)
    url_prepend = models.TextField(blank=True, null=True, default='', help_text='Add URL without trailing slash.')
    scrape = models.BooleanField(default=False)
    def __str__(self):
        return "%s" % (self.publication_name)

class Article(models.Model):
    issue = models.ForeignKey(Issue, blank=True, null=True, default=None, on_delete=models.PROTECT)
    publication_name = models.ForeignKey(Publication, blank=True, null=True, default='', on_delete=models.PROTECT)
    title = models.TextField()
    byline = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True, default=datetime.date(1900, 1, 1)) # Date published; from newspaper
    url = models.URLField(max_length=500, unique=True) # Added unique=True
    text = models.TextField(blank=True, null=True)
    scrape_date = models.DateField(blank=True, null=True, default=datetime.date(1900, 1, 1))
    scrape_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True,)
    topic_keywords = models.TextField(blank=True, null=True)
    # TODO: add entities_sentiment
    bias = models.IntegerField(default=50, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Select a number between 0 and 100, where 0 is extremely liberal, and 100 is extremely conservative.')
    display = models.BooleanField(default=False)
    def __str__(self):
        return "%s" % (self.title)