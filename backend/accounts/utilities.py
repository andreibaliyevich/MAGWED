from os.path import splitext
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils import timezone


def encode_uid(user_id):
    return force_str(urlsafe_base64_encode(force_bytes(user_id)))


def decode_uid(user_id):
    return force_str(urlsafe_base64_decode(user_id))


def make_token(user):
    return default_token_generator.make_token(user)


def check_token(user, token):
    return default_token_generator.check_token(user, token)


def get_avatar_path(instance, filename):
    """ Get path of avatar """
    path_name = timezone.now().strftime('%Y/%m/%d/%H%M%S%f')
    file_ext = splitext(filename)[1].lower()
    return f'avatars/{ path_name }{ file_ext }'
