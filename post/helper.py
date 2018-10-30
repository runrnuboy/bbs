from django.core.cache import cache


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
