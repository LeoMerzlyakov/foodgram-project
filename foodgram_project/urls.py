from api import urls as apiurls

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from recipes import urls as recipesurls
from . import views

from users import urls as userurls


urlpatterns = [
    path('', include(recipesurls,  namespace='recipes')),
    path('admin/', admin.site.urls),
    path('auth/', include(userurls, namespace='users')),
    path('api/', include(apiurls, namespace='api')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.page_not_found
handler403 = views.forbidden
handler400 = views.bed_request
handler500 = views.interall_error
