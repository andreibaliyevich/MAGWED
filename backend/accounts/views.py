from django.shortcuts import render


def index(request):
    """ Accounts page """
    context = {
        # 'title': _('index'),
    }
    return render(request, 'accounts/index.html', context)
