from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.pagination import LimitOffsetPagination

from rest_flex_fields import is_expanded
from rest_flex_fields.views import FlexFieldsMixin, FlexFieldsModelViewSet

from .serializers import ConstellationSerializer, ConstellationImageSerializer, \
    GalaxySerializer, GalaxyImageSerializer, PostSerializer, PostImageSerializer,\
    CommentSerializer
from .models import Constellation, ConstellationImage, Galaxy, GalaxyImage,\
    Post, PostImage, Comment


class IsOwnerOfObjectOrReadOnly(BasePermission):
    """
    The request is from the owner of the object, or is a read-only request.

    A custom permission class extending BasePermission.
    """

    def has_object_permission(self, request, view, obj):
        safe_methods = ('GET', 'HEAD', 'OPTIONS')
        if request.method in safe_methods:
            return True
        return obj.owner == request.user


class CustomLimitOffsetPagination(LimitOffsetPagination):
    """
    Sets the default page size to 10 and the maximum to 50.
    """

    # A numeric value indicating the limit to use if one is not provided by the
    # client in a query parameter.
    default_limit = 10

    # A value indicating the maximum allowable limit that may be requested by
    # the client.
    max_limit = 50


class AbstractCustomViewSet(FlexFieldsModelViewSet):
    """
    It provides full functionality for the authenticated owner of the object,
    and read-only options for all other users - authenticated or not.


    Extends FlexFieldModelViewSet and is able to dynamically set fields.

    Select a subset of fields by either:
    specifying which ones should be included

        e.g.  https://api.example.org/galaxies/?fields=pk,name

    specifying which ones should be excluded

        e.g.  https://api.example.org/galaxies/?omit=pk,name

    Easily set up fields that be expanded to their fully serialized counterparts
    via query parameters (users/?expand=organization,friends)

        e.g.  https://api.example.org/galaxies/?expand=images

    Use dot notation to dynamically modify fields at arbitrary depths

        e.g. https://api.example.org/constellations/?expand=galaxies.images


    Uses CustomLimitOffsetPagination with default page size of 10 and maximum
    of 50.

    This pagination style mirrors the syntax used when looking up multiple
    database records. The client includes both a "limit" and an "offset" query
    parameter.

    The limit indicates the maximum number of items to return.

    The offset indicates the starting position of the query in relation to the
    complete set of unpaginated items.

        e.g.  https://api.example.org/galaxies/?limit=40&offset=400
    """

    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOfObjectOrReadOnly,)
    pagination_class = CustomLimitOffsetPagination

    def perform_create(self, serializer):
        """
        Prevents an authenticated user creating a record with the id of another user.
        """
        serializer.save(owner=self.request.user)


class ConstellationViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    A viewset that provides read only functionality for the Constellation model.

    All other actions(create, update, destroy, etc.) are going to be available
    to superusers only through the admin panel.
    """

    serializer_class = ConstellationSerializer
    permit_list_expands = ['galaxies', 'images']
    pagination_class = CustomLimitOffsetPagination

    def get_queryset(self):
        queryset = Constellation.objects.all()

        if is_expanded(self.request, 'galaxies'):
            queryset = queryset.prefetch_related('galaxies')

        if is_expanded(self.request, 'images'):
            queryset = queryset.prefetch_related('images')

        return queryset


class ConstellationImageViewSet(FlexFieldsMixin, RetrieveModelMixin, GenericViewSet):
    """
    A viewset that provides read only functionality for the ConstellationImage model.

    All other actions(create, update, destroy, etc.) are going to be available
    to superusers only through the admin panel.
    """

    serializer_class = ConstellationImageSerializer
    queryset = ConstellationImage.objects.all()
    pagination_class = CustomLimitOffsetPagination


class GalaxyViewSet(AbstractCustomViewSet):
    """
    A viewset for the Galaxy model.

    Has 'images' as an expandable field.
    """
    __doc__ += AbstractCustomViewSet.__doc__

    serializer_class = GalaxySerializer
    permit_list_expands = ['images']

    def get_queryset(self):
        queryset = Galaxy.objects.all()

        if is_expanded(self.request, 'images'):
            queryset = queryset.prefetch_related('images')

        return queryset


class PostViewSet(AbstractCustomViewSet):
    """
    A viewset for the Post model.

    Has 'images' and 'comments' as expandable fields.
    """
    __doc__ += AbstractCustomViewSet.__doc__

    serializer_class = PostSerializer
    permit_list_expands = ['images', 'comments']

    def get_queryset(self):
        queryset = Post.objects.all()

        if is_expanded(self.request, 'images'):
            queryset = queryset.prefetch_related('images')

        if is_expanded(self.request, 'comments'):
            queryset = queryset.prefetch_related('comments')

        return queryset


class CommentViewSet(AbstractCustomViewSet):
    """
    A viewset for the Comment model.
    """
    __doc__ += AbstractCustomViewSet.__doc__

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class GalaxyImageViewSet(AbstractCustomViewSet):
    """
    A viewset for the GalaxyImage model.
    """
    __doc__ += AbstractCustomViewSet.__doc__

    serializer_class = GalaxyImageSerializer
    queryset = GalaxyImage.objects.all()


class PostImageViewSet(AbstractCustomViewSet):
    """
    A viewset for the PostImage model.
    """
    __doc__ += AbstractCustomViewSet.__doc__

    serializer_class = PostImageSerializer
    queryset = PostImage.objects.all()
