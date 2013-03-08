from chunkycms.models import Page, NewsPost, Chunk
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class ChunkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['slug', 'content', 'category']}),
    ]


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'content', 'author', 'parent']}),
        (_('Advanced Options'), {'fields': ['slug'], 'classes': ['collapse']})
    ]
    search_fields = ['title', 'content', 'slug']


class NewsPostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'content', 'author']}),
    ]

admin.site.register(Chunk, ChunkAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(NewsPost, NewsPostAdmin)
