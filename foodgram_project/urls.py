"""foodgram_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from users import urls as userurls
from recipes import urls as recipesurls
from api import urls as apiurls

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import (
handler400, handler403, handler404, handler500
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(userurls,  namespace='users')),
    path('api/', include(apiurls,  namespace='api')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include(recipesurls,  namespace='recipes')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
