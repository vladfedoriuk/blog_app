from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['sane_lists']))


@register.simple_tag(name="total_published")
def total_posts():
    return Post.published_posts.count()


@register.inclusion_tag(filename='app/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published_posts.order_by('-published')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag(name="most_commented_posts")
def get_most_commented_posts(count=5):
    return Post.published_posts.annotate(
        total_comments=Count("comments")
    ).order_by("-total_comments")[:count]
