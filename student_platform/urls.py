from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse


def test(request):
    return HttpResponse("URL WORKS")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test),

    path('parties/', include('parties.urls')),
    path('', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
