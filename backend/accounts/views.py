from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model, user_logged_in, user_logged_out
from django.utils.translation import ugettext_lazy as _
from .filters import OrganizerFilter
from .models import Organizer
from .pagination import OrganizerSetPagination
from .serializers import (
    RegistrationSerializer,
    UidAndTokenSerializer,
    PasswordChangeSerializer,
    OrganizerListSerializer,
    OrganizerDetailSerializer,
)


UserModel = get_user_model()


class LoginView(ObtainAuthToken):
    """ Login View """
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if created:
            user_logged_in.send(
                sender=user.__class__, request=request, user=user
            )
        return Response({'token': token.key})


class LogoutView(APIView):
    """ Logout View """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationView(generics.CreateAPIView):
    """ Registration View """
    queryset = UserModel.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class ActivationView(APIView):
    """ Activation View """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UidAndTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if user.is_active:
            return Response(
                {'detail': _('Stale token for given user.')},
                status=status.HTTP_403_FORBIDDEN)
        else:
            user.is_active = True
            user.save(update_fields=['is_active'])
            return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordChangeView(APIView):
    """ Password Change View """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'user': request.user},
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizerListView(generics.ListAPIView):
    """ Organizer List View """
    queryset = Organizer.objects.filter(user__is_active=True)
    serializer_class = OrganizerListSerializer
    pagination_class = OrganizerSetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrganizerFilter


class OrganizerDetailView(generics.RetrieveAPIView):
    """ Organizer Detail View """
    queryset = Organizer.objects.filter(user__is_active=True)
    lookup_field = 'profile_url'
    serializer_class = OrganizerDetailSerializer
