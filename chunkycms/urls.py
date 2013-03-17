from django.conf.urls import patterns, url


urlpatterns = patterns("",
                       url(r"^(?P<path>[0-9a-z/\-\.\_]+)/$",
                           "chunkycms.views.show_page", name="show_page"),
                       )
