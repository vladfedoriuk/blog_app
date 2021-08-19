from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post
from django.utils.safestring import mark_safe
import markdown


class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('app:post_list')
    description = 'New posts of my blog'

    def items(self):
        return Post.published_posts.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(
            mark_safe(
                markdown.markdown(item.body, extensions=['sane_lists'])
            ), 30)


