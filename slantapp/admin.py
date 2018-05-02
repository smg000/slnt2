from django.contrib import admin

class IssueAdmin(admin.ModelAdmin):
    list_display = ('issue', 'date', 'display', 'order')
    ordering = ('-display', 'issue', 'date',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('issue', 'publication_name', 'title', 'date', 'bias', 'display')
    ordering = ('-display', 'issue', 'title', 'date',)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('publication_name', 'url_root', 'publication_logo', 'scrape')
    ordering = ('publication_name',)

from .models import Issue
admin.site.register(Issue, IssueAdmin)

from .models import Article
admin.site.register(Article, ArticleAdmin)

from .models import Publication
admin.site.register(Publication, PublicationAdmin)