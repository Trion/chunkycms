from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
import json
from chunkycms.models import Page, NewsPost, Chunk, ChunkCategory


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

            form.base_fields['parent'].queryset = form.base_fields[
                'parent'].queryset.exclude(pk__in=successors_pks)

        return form

    def get_urls(self):
        """ overwrite urls to enable ajax support """
        urls = super(PageAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r"^change/(?P<pk>[0-9a-z/\-\.\_]+)/$",
                               self.admin_site.admin_view(self.ajax_change), name="chunkycms_page_change_ajax")
                           )
        return my_urls + urls

    def ajax_change(self, request, pk):
        """ view for ajax change requests """
        if request.method == "PUT":
            try:
                obj = self.model.objects.get(pk=pk)
            except Page.DoesNotExist:
                raise Http404()

            body = json.loads(request.body)
            for item in body:
                name = item.rsplit("/", 1)[-1][:-1]
                if hasattr(obj, name):
                    setattr(obj, name, body[item])
            obj.save()
            return HttpResponse()
        else:
            return redirect("admin:chunkycms_page_add", kwargs={"object_id": pk})


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

    def get_form(self, request, obj=None, **kwargs):
        form = super(CatAdmin, self).get_form(request, obj, **kwargs)

        # Filter successors from parent list, to prevent cycled hierarchies
        if obj is not None:
            successors = obj.successors
            successors_pks = [obj.pk]
            for category in successors:
                successors_pks.append(category.pk)

            form.base_fields['parent'].queryset = form.base_fields[
                'parent'].queryset.exclude(pk__in=successors_pks)

        return form

admin.site.register(ChunkCategory, CatAdmin)
