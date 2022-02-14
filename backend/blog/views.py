from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .models import ArticleImage


def index(request):
    """ Blog page """
    context = {
        # 'title': _('index'),
    }
    return render(request, 'blog/index.html', context)


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
