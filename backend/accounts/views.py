from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model, user_logged_in, user_logged_out
from django.core.cache import caches
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from .choices import UserType
from .filters import OrganizerFilter
from .models import Customer, Organizer, OrganizerLink
from .pagination import OrganizerPagination
from .permissions import UserIsOrganizer
from .serializers import (
    UserLoginSerializer,
    RegistrationSerializer,
    ActivationSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    UserProfileSerializer,
    CustomerProfileSerializer,
    ProfileAvatarSerializer,
    OrganizerCoverSerializer,
    OrganizerLinkSerializer,
    OrganizerProfileSerializer,
    OrganizerListSerializer,
    OrganizerDetailSerializer,
)
from .services import send_activation_email, send_password_reset_email


UserModel = get_user_model()


class LoginView(ObtainAuthToken):
    """ Login View """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)
        if created:
            user_logged_in.send(
                sender=user.__class__, request=request, user=user
            )

        user_data = UserLoginSerializer(
            user,
            context={'request': request},
        ).data
        user_data['token'] = token.key

        return Response(user_data)


class LogoutView(APIView):
    """ Logout View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationView(generics.CreateAPIView):
    """ Registration View """
    permission_classes = [AllowAny]
    queryset = UserModel.objects.all()
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_activation_email(user, self.request.LANGUAGE_CODE)


class ActivationView(APIView):
    """ Activation View """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ActivationSerializer(data=request.data)
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

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'user': request.user},
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetView(APIView):
    """ Password Reset View """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if user.has_usable_password():
            send_password_reset_email(user, request.LANGUAGE_CODE)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'detail': _('The user does not have a password.')},
                status=status.HTTP_403_FORBIDDEN)


class PasswordResetConfirmView(APIView):
    """ Password Reset Confirm View """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(APIView):
    """ Profile View """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == UserType.ADMIN:
            serializer = UserProfileSerializer(request.user)
        elif request.user.user_type == UserType.CUSTOMER:
            customer = get_object_or_404(Customer, user=request.user)
            serializer = CustomerProfileSerializer(customer)
        elif request.user.user_type == UserType.ORGANIZER:
            organizer = get_object_or_404(Organizer, user=request.user)
            serializer = OrganizerProfileSerializer(organizer)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        if request.user.user_type == UserType.ADMIN:
            serializer = UserProfileSerializer(request.user, data=request.data)
        elif request.user.user_type == UserType.CUSTOMER:
            customer = get_object_or_404(Customer, user=request.user)
            serializer = CustomerProfileSerializer(customer, data=request.data)
        elif request.user.user_type == UserType.ORGANIZER:
            organizer = get_object_or_404(Organizer, user=request.user)
            serializer = OrganizerProfileSerializer(
                organizer, data=request.data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAvatarView(APIView):
    """ Profile Avatar View """
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ProfileAvatarSerializer(
            request.user,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        request.user.avatar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizerCoverView(APIView):
    """ Organizer Cover View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]

    def get(self, request, *args, **kwargs):
        organizer = get_object_or_404(Organizer, user=request.user)
        serializer = OrganizerCoverSerializer(
            organizer,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        organizer = get_object_or_404(Organizer, user=request.user)
        serializer = OrganizerCoverSerializer(
            organizer,
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        organizer = get_object_or_404(Organizer, user=request.user)
        organizer.cover.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrganizerLinkListCreateView(generics.ListCreateAPIView):
    """ Organizer Link List or Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = OrganizerLinkSerializer

    def get_queryset(self):
        organizer = get_object_or_404(Organizer, user=self.request.user)
        queryset = OrganizerLink.objects.filter(organizer=organizer)
        return queryset

    def perform_create(self, serializer):
        organizer = get_object_or_404(Organizer, user=self.request.user)
        serializer.save(organizer=organizer)


class OrganizerLinkRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Organizer Link Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = OrganizerLinkSerializer

    def get_queryset(self):
        organizer = get_object_or_404(Organizer, user=self.request.user)
        queryset = OrganizerLink.objects.filter(organizer=organizer)
        return queryset


class WebSocketAuthTokenView(APIView):
    """ WebSocket Auth Token View """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        wstoken = get_random_string(length=32)

        wstokens_cache = caches['wstokens']
        wstokens_cache.set(wstoken, request.user.id)

        return Response({'wstoken': wstoken})


class OrganizerListView(generics.ListAPIView):
    """ Organizer List View """
    queryset = Organizer.objects.filter(user__is_active=True)
    serializer_class = OrganizerListSerializer
    pagination_class = OrganizerPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrganizerFilter


class OrganizerDetailView(generics.RetrieveAPIView):
    """ Organizer Detail View """
    queryset = Organizer.objects.filter(user__is_active=True)
    lookup_field = 'profile_url'
    serializer_class = OrganizerDetailSerializer
