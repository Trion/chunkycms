from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from chunkycms.models import Page


def show_page(request, path):
    """ shows a page """

    try:
        page = Page.get_by_path(path)
    except Page.DoesNotExist:
        raise Http404

    return render_to_response("chunkycms/page.html", context_instance=RequestContext(request, {'page': page}))
