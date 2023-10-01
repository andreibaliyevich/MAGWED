from rest_framework import generics
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .models import Category, Article, ArticleImage
from .pagination import ArticlePagination
from .serializers import (
    CategoryListSerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
)


class CategoryListView(generics.ListAPIView):
    """ Category List View """
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class ArticleListView(generics.ListAPIView):
    """ Article List View """
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    pagination_class = ArticlePagination


class ArticleDetailView(generics.RetrieveAPIView):
    """ Article Detail View """
    queryset = Article.objects.all()
    lookup_field = 'slug'
    serializer_class = ArticleDetailSerializer


@require_POST
@csrf_protect
def article_upload_image(request):
    """ Article upload Image """
    if request.FILES:
        article_image = ArticleImage()
        article_image.file = request.FILES['file']
        article_image.save()
        return JsonResponse({'location': article_image.file.url})
    else:
        return HttpResponse(_('Form not valid!'), status=400)
