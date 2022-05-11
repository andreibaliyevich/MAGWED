from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model, user_logged_in, user_logged_out
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from .filters import OrganizerFilter
from .models import Customer, Organizer
from .pagination import OrganizerSetPagination
from .serializers import (
    UserLoginSerializer,
    RegistrationSerializer,
    UidAndTokenSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    UserProfileSerializer,
    CustomerProfileSerializer,
    OrganizerProfileSerializer,
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

        response_data = {'token': token.key}
        user_serializer = UserLoginSerializer(user)
        response_data.update(user_serializer.data)

        return Response(response_data)


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
    permission_classes = [AllowAny]
    queryset = UserModel.objects.all()
    serializer_class = RegistrationSerializer


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
    authentication_classes = [TokenAuthentication]
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


class PasswordResetView(APIView):
    """ Password Reset View """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if user.has_usable_password():
            serializer.send_password_reset_email()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'detail': _('The user does not have a password.')},
                status=status.HTTP_403_FORBIDDEN)


class PasswordResetConfirmView(APIView):
    """ Password Reset Confirm View """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type == 1:
            serializer = UserProfileSerializer(request.user)
        elif request.user.user_type == 2:
            customer = get_object_or_404(Customer, user=request.user)
            serializer = CustomerProfileSerializer(customer)
        elif request.user.user_type == 3:
            organizer = get_object_or_404(Organizer, user=request.user)
            serializer = OrganizerProfileSerializer(organizer)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        if request.user.user_type == 1:
            serializer = UserProfileSerializer(request.user, data=request.data)
        elif request.user.user_type == 2:
            customer = get_object_or_404(Customer, user=request.user)
            serializer = CustomerProfileSerializer(customer, data=request.data)
        elif request.user.user_type == 3:
            organizer = get_object_or_404(Organizer, user=request.user)
            serializer = OrganizerProfileSerializer(
                organizer, data=request.data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
