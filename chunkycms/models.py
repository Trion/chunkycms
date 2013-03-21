from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings


class SelfParent(Exception):

    def __init__(self):
        super(SelfParent, self).__init__('Object cannot be ancestor of itself')


class AlreadyExist(Exception):

    def __init__(self):
        super(AlreadyExist, self).__init__('Object already exist in namespace')


class Content(models.Model):
    """
    abstract model for models with content
    """
    content = models.TextField(_('Content'))
    author = models.ForeignKey(User, verbose_name=_('author'))
    created_on = models.DateField(_('Created On'), auto_now_add=True)
    changed_on = models.DateField(_('Changed On'), auto_now=True)

    class Meta:
        abstract = True


class Hierarchical(models.Model):
    """
    abtract model for hierachical structures
    """
    slug = models.CharField(_('Slug'), max_length=150, blank=True)
    parent = models.ForeignKey('self', verbose_name=_('Parent'), null=True, blank=True)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        setattr(self, 'AlreadyExist', AlreadyExist)
        setattr(self, 'SelfParent', SelfParent)
        super(Hierarchical, self).__init__(*args, **kwargs)

    def level_unique(self):
        """
        Check whether name already exist in namespace
        """

        twins = self.siblings.filter(slug=self.slug)
        if (twins.count() > 0 and twins[0].pk != self.pk):
            return False

        return True

    def is_ancestor(self, child):
        """
        checks whether the object is an ancestor of the given child

        @param child a hierachical object
        """

        ancestor = child.parent
        while ancestor:
            if self.pk == ancestor.pk:
                return True
            ancestor = ancestor.parent

        return False

    @property
    def siblings(self):
        """
        a queryset with all chunks with the same category
        """
        return self.__class__.objects.filter(parent=self.parent)

    @property
    def name(self):
        """ title or slug, depending on type """
        if hasattr(self, "title"):
            return self.title
        else:
            return self.slug

    @property
    def children(self):
        """ a list of children """
        pass


class ChunkCategory(Hierarchical):

    class Meta:
        verbose_name = _('Chunk Category')
        verbose_name_plural = _('Chunk Categories')

    def __unicode__(self):
        return self.name

    def save(self, **kwargs):
        if not self.level_unique():
            raise self.AlreadyExist

        if self.is_ancestor(self):
            raise self.SelfParent

        super(ChunkCategory, self).save(**kwargs)

    @property
    def children(self):
        return list(self.chunkcategory_set.all()) + list(self.chunk_set.all())

    @property
    def successors(self):
        """ returns a queryset with all succsessors of the type ChunkCategory """

        # Maybe theres a better way to flatten hierachies in models
        queryset = self.chunkcategory_set.all()
        for category in queryset:
            queryset = queryset | category.chunkcategory_set.all()

        return queryset


class Chunk(Content):
    slug = models.CharField(_('Slug'), max_length=150)
    category = models.ForeignKey(ChunkCategory, verbose_name=_('Category'), null=True, blank=True)

    class Meta:
        verbose_name = _('Chunk')
        verbose_name_plural = _('Chunks')

    def __unicode__(self):
        return self.slug

    def save(self, **kwargs):

        twins = Chunk.objects.filter(category=self.category).filter(slug=self.slug)
        if twins.count() > 0 and twins[0].pk != self.pk:
            raise self.AlreadyExist

        super(Chunk, self).save(**kwargs)

    @property
    def name(self):
        return self.slug


class Post(Content):
    title = models.CharField(_('Title'), max_length=150)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        abstract = True

    def __unicode__(self):
        return self.title

    def save(self, **kwargs):
        # Generate slug from title
        if not self.slug:
            slug = ''
            # Clean title from special characters
            for char in self.title:
                if char == ' ':
                    slug += '-'
                else:
                    if char.isalnum():
                        slug += char
                self.slug = slug

        self.slug = self.slug.replace(u'\xe4', 'ae').replace(u'\xfc', 'ue').replace(u'\xf6', 'oe').replace(u'\xdf', 'ss')
        self.slug = self.slug.lower()

        # Add suffix number, if slug already exist
        try:
            post = self.lvl_query_set.get(slug=self.slug)
            if post.pk != self.pk:
                self.gen_alt_slug()
        except self.__class__.DoesNotExist:
            pass

        super(Post, self).save(**kwargs)

    def gen_alt_slug(self):
        """ Generates an alternative slug. It appends a number to the old slug. """

        posts = self.lvl_query_set.filter(slug=self.slug)
        i = 0
        while posts.count() > 0:
            i += 1
            slug = self.slug + str(i)
            posts = self.lvl_query_set.filter(slug=slug)

        self.slug = slug


class Page(Post, Hierarchical):
    template = models.CharField(_("Template"), max_length=250, choices=settings.CHUNKYCMS_TEMPLATES, default="chunkycms/page.html")

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def save(self, **kwargs):
        if not self.level_unique():
            raise self.AlreadyExist

        if self.is_ancestor(self):
            raise self.SelfParent

        super(Page, self).save(**kwargs)

    @property
    def lvl_query_set(self):
        """ proterty which contains a query set with all pages on the same level """
        if self.parent:
            return self.parent.page_set
        else:
            return Page.objects.filter(parent=None)

    @property
    def path(self):
        """ returns hiearchical path of the page """

        page = self
        path = ""
        while page.parent is not None:
            path = "/" + page.slug + path
            page = page.parent

        path = page.slug + path
        return path

    @property
    def successors(self):
        """ returns a queryset with all succsessors of a page """

        # Maybe theres a better way to flatten hierachies in models
        queryset = self.page_set.all()
        for page in queryset:
            queryset = queryset | page.page_set.all()

        return queryset

    @property
    def children(self):
        return list(self.page_set.all())

    @classmethod
    def get_by_path(cls, path):
        """ returns page by path (slug hierarchy) """

        slugs = path.split("/")
        parent = cls.objects.get(slug=slugs[0], parent=None)
        del slugs[0]

        for slug in slugs:
            parent = parent.page_set.get(slug=slug)

        return parent


class NewsPost(Post):
    slug = models.CharField(_('Slug'), max_length=150, blank=True)

    class Meta:
        verbose_name = _('News Post')
        verbose_name_plural = _('News Posts')

    @property
    def lvl_query_set(self):
        return NewsPost.objects.all()
