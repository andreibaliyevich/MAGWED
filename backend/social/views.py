from django.shortcuts import render


def index(request):
    """ Social page """
    context = {
        # 'title': _('index'),
    }
    return render(request, 'social/index.html', context)
