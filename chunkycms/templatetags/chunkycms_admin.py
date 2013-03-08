from django.template import Library
from chunkycms.models import Page

register = Library()


@register.inclusion_tag('admin/chunkycms/page/tag_page_tree.html')
def page_tree(parent=None):

    if not parent:
        pages = Page.objects.filter(parent=None)
    else:
        pages = parent.page_set.all()

    return {'pages': pages}
