import random
import string


def content_file_name(instance, filename):
    try:
        extension = filename.split('.')[-1]
    except:
        extension = 'jpg'
    extension = "jpg" if extension == "jpeg" else extension
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    random_string = code + "." + extension
    model_name = ''
    try:
        model_name = type(instance).__name__
    except:
        pass
    name = ''
    if model_name == 'User':
        name = instance.idx
        name = '/'.join(['profile_pics', name, random_string])
    else:
        name = '/'.join(['extra', random_string])
    return name


def content_icon_name(instance, filename):
    try:
        extension = filename.split('.')[-1]
    except:
        extension = 'jpg'
    extension = "jpg" if extension == "jpeg" else extension
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    random_string = code + "." + extension
    model_name = ''
    try:
        model_name = type(instance).__name__
    except:
        pass
    name = '/'.join(['extra', random_string])
    return name


def url_builder(obj, request):
    build_url = None
    try:
        from project.settings import PROXY_URL, MEDIA_URL
        # if request is not None:
        #     url = request.build_absolute_uri(obj.url)
        # else:
        #     url = obj.url if obj else None
        url = None
        if isinstance(obj, str):
            len_media = len(MEDIA_URL)
            url = obj if obj[:len_media] == MEDIA_URL else MEDIA_URL + obj
        else:
            url = obj.url
        build_url = PROXY_URL + url
    except Exception as e:
        build_url = None
    return build_url
