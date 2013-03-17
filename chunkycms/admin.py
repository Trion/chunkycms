from chunkycms.models import Page, NewsPost, Chunk, ChunkCategory
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class ChunkAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['slug', 'content', 'category', 'author']}),
    ]
    search_fields = ['content', 'slug']

    def get_form(self, request, obj=None, **kwargs):
        form = super(ChunkAdmin, self).get_form(request, obj, **kwargs)

        # Set default author for new page
        if obj is None:
            form.base_fields['author'].initial = request.user.id

        return form


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'content',
         'author', 'parent']}),
        (_('Advanced Options'), {'fields': ['slug'], 'classes': ['collapse']})
    ]
    search_fields = ['title', 'content', 'slug']

    def get_form(self, request, obj=None, **kwargs):
        form = super(PageAdmin, self).get_form(request, obj, **kwargs)

        # Set default author for new page
        if obj is None:
            form.base_fields['author'].initial = request.user.id

        # Filter successors from parent list, to prevent cycled hierarchies
        if obj is not None:
            successors = obj.successors
            successors_pks = [obj.pk]
            for page in successors:
                successors_pks.append(page.pk)

            form.base_fields['parent'].queryset = form.base_fields['parent'].queryset.exclude(pk__in=successors_pks)

        return form


class NewsPostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'content', 'author']}),
    ]

admin.site.register(Chunk, ChunkAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(NewsPost, NewsPostAdmin)


class CatAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['slug', 'parent']}),
    ]
admin.site.register(ChunkCategory, CatAdmin)
