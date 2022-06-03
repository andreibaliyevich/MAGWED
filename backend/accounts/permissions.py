from rest_framework import permissions
from django.utils.translation import gettext_lazy as _
from .choices import UserType


class OrganizerPermission(permissions.BasePermission):
    """ Permission check. User is Organizer. """
    message = _('Only organizers have permission.')

    def has_permission(self, request, view):
        if request.user.user_type == UserType.ORGANIZER:
            return True
        else:
            return False
