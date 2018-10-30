from math import ceil

from django.core.cache import cache
from django.shortcuts import render, redirect

from post.models import Post
from post.helper import page_cache


@page_cache
def post_list(request):
    page = int(request.GET.get('page', 1))  # 当前页码
    per_page = 10                           # 每页文章数
    total = Post.objects.count()            # 帖子总数
    pages = ceil(total / per_page)          # 总页数

    start = (page - 1) * 10
    end = start + 10
    posts = Post.objects.all()[start:end]
    return render(request, 'post_list.html',
                  {'posts': posts, 'pages': range(pages)})


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    return render(request, 'create_post.html')


def edit_post(request):
    if request.method == 'POST':
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(pk=post_id)
        post.title = request.POST.get('title').strip()
        post.content = request.POST.get('content').strip()
        post.save()

        # 更新缓存
        key = 'Post-%s' % post_id
        cache.set(key, post)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = int(request.GET.get('post_id'))
        post = Post.objects.get(pk=post_id)
        return render(request, 'edit_post.html', {'post': post})


def read_post(request):
    post_id = int(request.GET.get('post_id'))
    key = 'Post-%s' % post_id
    post = cache.get(key)  # 先从缓存里取数据
    print('get from cache: %s' % post)
    if post is None:
        post = Post.objects.get(pk=post_id)  # 缓存里没有，直接从数据库获取数据
        print('get from db: %s' % post)
        cache.set(key, post)                 # 将数据存入缓存，方便以后使用
        print('set data into cache')
    return render(request, 'read_post.html', {'post': post})


def delete_post(request):
    post_id = int(request.GET.get('post_id'))
    Post.objects.get(pk=post_id).delete()
    return redirect('/')
