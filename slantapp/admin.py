from django.contrib import admin

class IssueAdmin(admin.ModelAdmin):
    list_display = ('issue', 'date', 'display', 'order')
    ordering = ('-display', 'issue', 'date',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('issue', 'publication_name', 'title', 'date', 'bias', 'display')
    ordering = ('-display', 'issue', 'title', 'date',)

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('publication_name', 'publication_logo')
    ordering = ('publication_name',)

class SiteAdmin(admin.ModelAdmin):
    list_display =  ('publication_name', 'url_full')

from .models import Issue
admin.site.register(Issue, IssueAdmin)

from .models import Article
admin.site.register(Article, ArticleAdmin)

from .models import Publication
admin.site.register(Publication, PublicationAdmin)

from .models import Site
admin.site.register(Site, SiteAdmin)