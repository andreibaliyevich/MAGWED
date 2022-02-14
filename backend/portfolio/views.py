from django.shortcuts import render


def index(request):
    """ Portfolio page """
    context = {
        # 'title': _('index'),
    }
    return render(request, 'portfolio/index.html', context)
