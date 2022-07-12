from os.path import splitext
from django.utils import timezone


def get_conversation_path(instance, filename):
    """ Get path of Conversation """
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'conversations/{ path_name }{ file_ext }'


def get_image_message_path(instance, filename):
    """ Get path of Image Message """
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'messages/images/{ path_name }{ file_ext }'


def get_file_message_path(instance, filename):
    """ Get path of File Message """
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'messages/files/{ path_name }{ file_ext }'
