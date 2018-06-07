from django.contrib import admin

class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'date', 'stage', 'display', 'order')
    ordering = ('-display', 'issue', 'date',)
    readonly_fields = ('id',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('issue', 'publication_name', 'title', 'scrape_date', 'bias', 'topic_keywords', 'display')
    ordering = ('-scrape_date', '-display', 'issue', 'title',)
    list_filter = (
        ('display', admin.BooleanFieldListFilter),
        ('date', admin.DateFieldListFilter),
        ('issue', admin.RelatedFieldListFilter),
    )
    search_fields = ['topic_keywords', 'title']

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('publication_name', 'url_root', 'publication_logo', 'scrape')
    ordering = ('publication_name',)

from .models import Issue
admin.site.register(Issue, IssueAdmin)

from .models import Article
admin.site.register(Article, ArticleAdmin)

from .models import Publication
admin.site.register(Publication, PublicationAdmin)