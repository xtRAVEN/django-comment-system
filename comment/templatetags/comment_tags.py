from django import template
from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static

from comment import settings

register = template.Library()


@register.inclusion_tag('utils/IMPORTS.html')
def render_imports():
    return {'offline_imports': settings.COMMENT_OFFLINE_IMPORTS}


@register.inclusion_tag('comment/comments.html')
def render_comments(request, obj):
    context = {
        'object': obj,
        'request': request,
        'object_info': {
            'app_name': type(obj)._meta.app_label,
            'model_name': type(obj).__name__,
            'content_type': ContentType.objects.get_for_model(obj),
            'object_id': obj.id
        }
    }
    return context


@register.simple_tag
def get_settings(settings_parameter):
    return getattr(settings, settings_parameter)


@register.simple_tag
def get_profile_image(user):
    if settings.COMMENT_PROFILE_IMAGE_FIELD:
        profile = getattr(user, settings.COMMENT_PROFILE_IMAGE_FIELD)
        if profile:
            return profile.url
        else:
            return static(settings.COMMENT_PROFILE_IMAGE_DEFAULT)
    else:
        return None


@register.filter
def number(value, floating_points=None):
    converters = {
        3: 'K',
        6: 'M',
        9: 'B',
    }

    if floating_points is not None and (10 ** 12 > value >= 1000):
        for exponent, converter in converters.items():
            large_number = 10 ** exponent
            if value >= large_number * 1000:
                continue
            return f'{value / large_number:,.{floating_points}f} {converter}'
    else:
        return f'{value:,}'


@register.filter
def to_range(end, start=1):
    return range(start, end + 1)


@register.simple_tag
def get_pagination(paginator):

    if paginator.paginator.num_pages <= 9:
        return paginator.paginator.page_range
    else:
        if paginator.number <= 5:
            return [*range(1, 7), 0, paginator.paginator.num_pages]
        elif paginator.number > paginator.paginator.num_pages - 5:
            return [1, 0, *range(paginator.paginator.num_pages - 5, paginator.paginator.num_pages + 1)]
        else:
            return [1, 0, paginator.number - 2, paginator.number - 1, paginator.number, paginator.number + 1, paginator.number + 2, 0, paginator.paginator.num_pages]
