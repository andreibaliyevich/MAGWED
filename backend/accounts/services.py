from django.utils import timezone


def check_pro_account(user):
    """ Check user is a professional account """
    if timezone.now() < user.organizer.pro_time:
        return True
    else:
        return False
