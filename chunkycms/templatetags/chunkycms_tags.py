from django.template import Library, RequestContext
from chunkycms.models import Chunk

register = Library()


@register.inclusion_tag('chunkycms/tag_chunk.html')
def chunk(request, chunkpath):
    """
    renders a chunk

    request is the current request object
    chunkpath is the path of the chunk
    """

    context = {
        "chunk": Chunk.get_by_path(chunkpath)
    }
    return RequestContext(request, context)
