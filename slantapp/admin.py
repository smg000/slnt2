from django.contrib import admin

class IssueAdmin(admin.ModelAdmin):
    list_display = ('issue', 'date', 'display', 'order')

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('issue', 'publication_name', 'title', 'date', 'bias', 'display')

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('publication_name', 'publication_logo')

from .models import Issue
admin.site.register(Issue, IssueAdmin)

from .models import Article
admin.site.register(Article, ArticleAdmin)

from .models import Publication
admin.site.register(Publication, PublicationAdmin)

