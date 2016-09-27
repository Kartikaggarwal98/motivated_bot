from django.conf.urls import patterns, include, url
from django.contrib import admin
from redditbot.views import RedditBotView,index
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'motivate.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',index),
    url(r'^facebook_auth/?$',RedditBotView.as_view()),
)
