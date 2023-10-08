from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .filters import ArticleFilter
from .models import Article, BlogImage
from .pagination import ArticlePagination
from .serializers import (
    ArticleListSerializer,
    ArticleDetailSerializer,
)


class ArticleListView(generics.ListAPIView):
    """ Article List View """
    permission_classes = [AllowAny]
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    pagination_class = ArticlePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter


class ArticleDetailView(generics.RetrieveAPIView):
    """ Article Detail View """
    permission_classes = [AllowAny]
    queryset = Article.objects.all()
    lookup_field = 'slug'
    serializer_class = ArticleDetailSerializer


class ArticleUpViewCountView(APIView):
    """ Article Up View Count View """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Article, slug=kwargs['slug'])
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return Response(status=status.HTTP_204_NO_CONTENT)


@require_POST
@csrf_protect
def upload_image(request):
    """ Upload Image """
    if request.FILES:
        image = BlogImage()
        image.file = request.FILES['file']
        image.save()
        return JsonResponse({'location': image.file.url})
    else:
        return HttpResponse(_('Form not valid!'), status=400)
