from django.core.cache import cache

from common import rds
from post.models import Post


def page_cache(view_func):
    def wrapper(request):
        if request.method == 'GET':
            key = 'PageCache-%s' % request.get_full_path()
            response = cache.get(key)
            if response is None:
                response = view_func(request)
                cache.set(key, response)
        else:
            response = view_func(request)
        return response
    return wrapper


def get_top_n(num):
    '''获取阅读排行前 N 的文章'''
    # ori_data = [
    #     (b'16', 53.0),
    #     (b'27', 39.0),
    #     (b'31', 37.0),
    # ]
    ori_data = rds.zrevrange('ReadCounter', 0, num - 1, withscores=True)

    # cleaned_data = [
    #     [16, 53],
    #     [27, 39],
    #     [31, 37],
    # ]
    cleaned_data = [[int(post_id), int(count)] for post_id, count in ori_data]

    # 方法一
    for item in cleaned_data:
        key = 'Post-%s' % item[0]
        post = cache.get(key)
        if post is None:
            post = Post.objects.get(pk=item[0])
        item[0] = post

    # 方法二
    # post_id_list = [post_id for post_id, _ in cleaned_data]
    # posts = Post.objects.filter(id__in=post_id_list)
    # posts = sorted(posts, key=lambda post: post_id_list.index(post.id))  # 按照post_id_list的顺序进行排序
    # for index, item in enumerate(cleaned_data):
    #     item[0] = posts[index]

    # for post, item in zip(posts, cleaned_data):
    #     item[0] = post

    # 方法三
    post_id_list = [post_id for post_id, _ in cleaned_data]
    posts = Post.objects.in_bulk(post_id_list)
    for item in cleaned_data:
        post_id = item[0]
        item[0] = posts[post_id]

    return cleaned_data
