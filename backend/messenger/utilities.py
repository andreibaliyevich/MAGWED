from os.path import splitext
from django.utils import timezone


def get_conversation_path(instance, filename):
    """ Get path of Conversation """
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'conversations/{ path_name }{ file_ext }'
