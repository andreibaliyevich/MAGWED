from os.path import splitext
from django.utils import timezone


def get_cover_path(instance, filename):
    """ Get path of cover """
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'covers/{ path_name }{ file_ext }'


def get_thumbnail_path(instance, filename):
    """ Get path of thumbnail """
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'thumbnails/{ path_name }{ file_ext }'
