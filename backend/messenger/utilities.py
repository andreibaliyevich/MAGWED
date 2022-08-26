from os.path import splitext
from django.utils import timezone


def get_conversation_path(instance, filename):
    """ Get path of Conversation """
    filepath = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'conversations/{ filepath }{ file_ext }'


def get_image_message_path(instance, filename):
    """ Get path of Image Message """
    filepath = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'messages/images/{ filepath }{ file_ext }'


def get_file_message_path(instance, filename):
    """ Get path of File Message """
    filepath = timezone.now().strftime('%Y/%m/%d/')
    return f'messages/files/{ filepath }{ filename }'
