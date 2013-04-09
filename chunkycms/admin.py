from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
import json
from chunkycms.models import Page, NewsPost, Chunk, ChunkCategory


class LiveAdmin(admin.ModelAdmin):
    """ base class for live editiable models """

    def get_urls(self):
        """ overwrite urls to enable ajax support """
        urls = super(LiveAdmin, self).get_urls()
        url_name = "chunkycms_%s_change_ajax" % self.model.__name__.lower()
        my_urls = patterns('',
                           url(r"^change/(?P<pk>[0-9]+)/$",
                               self.admin_site.admin_view(self.ajax_change), name=url_name)
                           )
        return my_urls + urls

    def ajax_change(self, request, pk):
        """ view for ajax change requests """

        if request.is_ajax():
            if request.method == "PUT":
                try:
                    obj = self.model.objects.get(pk=pk)
                except Page.DoesNotExist:
                    raise Http404()

                attr = self.json_to_dict(request.body)
                for attr_name in attr:
                    setattr(obj, attr_name, attr[attr_name])
                obj.save()

                return HttpResponse()
            elif request.method == "GET":
                #TODO create ajax get view
                pass
            elif request.method == "POST":
                #TODO ajax creation view
                pass
        else:
            redirect_target = "admin:chunkycms_%s_change" % self.model.__name__.lower()
            return redirect(redirect_target, pk)

    def json_to_dict(self, body):
        """ converts a given body (json formatted) to a dictionary with possible model attributes """

        dict_body = json.loads(body)
        result_dict = {}
        for item in dict_body:
            # Skip meta data
            if item.startswith("@"):
                continue
            # Strip unnecessary parts
            attr_name = item.rsplit("/", 1)[-1][:-1]
            result_dict[attr_name] = dict_body[item]

        return result_dict


class ChunkAdmin(LiveAdmin):
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


class PageAdmin(LiveAdmin):
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
