
from django.contrib import admin
from django.urls import path,include
from authentication.views import home

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/",include("authentication.urls")),
    path('student/',include("student.urls")),
    path('warden/',include("warden.urls")),
    path('security/',include("security.urls")),
    path("",home,name="home")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


