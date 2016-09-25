from django.contrib.auth.views import logout as django_logout


def logout(request):
    return django_logout(request, next_page='/')
