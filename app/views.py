from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger

from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count, Subquery
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery


class PostListView(ListView):
    queryset = Post.published_posts.all()  # model = Post -> queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'app/post/list.html'


def post_list(request, tag_slug=None):
    posts = Post.published_posts.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__pk=tag.pk)

    paginator = Paginator(posts, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'app/post/list.html',
                  {
                      'page': page,
                      'posts': posts,
                      'tag': tag
                  })


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        status='published',
        published__year=year,
        published__month=month,
        published__day=day,
        slug=post_slug
    )
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create a Comment object but don't save to the database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the form
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values('id')
    similar_posts = Post.published_posts.filter(tags__in=Subquery(post_tags_ids)) \
                        .exclude(id=post.id) \
                        .annotate(same_tags_count=Count('tags')) \
                        .order_by('-same_tags_count', '-published')[:4]

    return render(
        request,
        'app/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts
        }
    )


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status='published'
    )
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" + cd.get('comments', '')
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
            # ... send email
    else:
        form = EmailPostForm()
    return render(request,
                  'app/post/share.html',
                  {
                      'post': post,
                      'form': form,
                      'sent': sent
                  }
                  )


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # results = Post.published_posts.annotate(
            #     search=SearchVector('title', 'body')
            # ).filter(search=query)
            #
            # search_vector = SearchVector('title', 'body')
            # search_query = SearchQuery(query)
            # results = Post.published_posts.annotate(
            #     search=search_vector,
            #     rank=SearchRank(search_vector, search_query)
            # ).filter(search=search_query).order_by('-rank')
            #
            search_vector = SearchVector('title', weight='A') + \
                SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published_posts.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
    return render(
        request,
        'app/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results,
        }
    )
