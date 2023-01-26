# for django dev server to serve media
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from galaxies.views import ConstellationViewSet, ConstellationImageViewSet,\
    GalaxyViewSet, PostViewSet, GalaxyImageViewSet, PostImageViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'constellations', ConstellationViewSet, basename='Constellations')
router.register(r'galaxies', GalaxyViewSet, basename='Galaxies')
router.register(r'posts', PostViewSet, basename='Posts')
router.register(r'comments', CommentViewSet, basename='Comments')
router.register(r'constellation_images', ConstellationImageViewSet, basename='Constellation Images')
router.register(r'galaxy_images', GalaxyImageViewSet, basename='Galaxy Images')
router.register(r'post_images', PostImageViewSet, basename='Post Images')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('my_auth.urls')),
    path('', include(router.urls)),
]

# for django dev server to serve media
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
