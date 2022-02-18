from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .models import Category, Article, ArticleImage
from .serializers import (
    CategoryListSerializer,
    CategoryDetailSerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
)


class CategoryListView(APIView):
    """ Category List View """

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailView(APIView):
    """ Category Detail View """

    def get(self, request, slug):
        category = Category.objects.get(slug=slug)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)


class ArticleListView(APIView):
    """ Article List View """

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)


class ArticleDetailView(APIView):
    """ Article Detail View """

    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)


@require_POST
@csrf_protect
def article_upload_image(request):
    """ Article upload Image """
    if request.FILES:
        article_image = ArticleImage()
        article_image.file = request.FILES['file']
        article_image.save()
        return JsonResponse({ 'location': article_image.file.url })
    else:
        return HttpResponse(_('Form not valid!'), status=400)
