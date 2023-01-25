from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_flex_fields import is_expanded
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet

from .serializers import ConstellationSerializer, ConstellationImageSerializer, \
    GalaxySerializer, GalaxyImageSerializer, PostSerializer, PostImageSerializer,\
    CommentSerializer
from .models import Constellation, ConstellationImage, Galaxy, GalaxyImage,\
    Post, PostImage, Comment


class ConstellationViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    serializer_class = ConstellationSerializer
    permit_list_expands = ['galaxies']

    def get_queryset(self):
        queryset = Constellation.objects.all()

        if is_expanded(self.request, 'galaxies'):
            queryset = queryset.prefetch_related('galaxies')

        return queryset


class ConstellationImageViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    serializer_class = ConstellationImageSerializer
    queryset = ConstellationImage.objects.all()


class GalaxyViewSet(FlexFieldsModelViewSet):
    serializer_class = GalaxySerializer
    permit_list_expands = ['images']

    def get_queryset(self):
        queryset = Galaxy.objects.all()

        if is_expanded(self.request, 'images'):
            queryset = queryset.prefetch_related('images')

        return queryset


class GalaxyImageViewSet(FlexFieldsModelViewSet):
    serializer_class = GalaxyImageSerializer
    queryset = GalaxyImage.objects.all()
