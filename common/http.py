from json import dumps

from django.conf import settings
from django.http import HttpResponse


def render_json(data=None, status_code=0):
    '''将返回值渲染为 JSON 数据'''
    result = {
        'data': data,      # 返回给前端的数据
        'sc': status_code  # 状态码
    }

    if settings.DEBUG:
        # Debug 模式时，按规范格式输出 json
        json_str = dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        # 正式环境下，将返回数据压缩
        json_str = dumps(result, ensure_ascii=False, separators=[',', ':'])

    print(json_str)

    return HttpResponse(json_str)
