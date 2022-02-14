from django.shortcuts import render


def index(request):
    """ Home page """
    context = {
        # 'title': _('index'),
    }
    return render(request, 'main/index.html', context)
