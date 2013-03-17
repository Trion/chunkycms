from django.template import loader, Context, Library
from chunkycms.models import Page, ChunkCategory, Chunk

register = Library()


@register.inclusion_tag('admin/chunkycms/tag_hierarchy_tree.html')
def hierarchy_tree(parent=None):
    """ generates hierarchy tree """

    if parent == "Page":
        nodes = Page.objects.filter(parent=None)
    elif parent == "Chunk":
        # dirty hack, to merge querysets of different models
        nodes = list(ChunkCategory.objects.filter(parent=None)) + list(Chunk.objects.filter(category=None))
    else:
        if hasattr(parent, "children"):
            nodes = parent.children
        else:
            nodes = None

    return {"nodes": nodes}


@register.simple_tag
def node_menu(node):
    """ generates node menu """

    if node.__class__.__name__ == "Page":
        template = "admin/chunkycms/page/tag_page_menu.html"
    elif node.__class__.__name__ == "Chunk":
        template = "admin/chunkycms/chunk/tag_chunk_menu.html"
    elif node.__class__.__name__ == "ChunkCategory":
        template = "admin/chunkycms/chunkcategory/tag_chunkcategory_menu.html"

    context = Context({"node": node})
    return loader.get_template(template).render(context)
