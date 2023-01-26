from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.viewsets import ReadOnlyModelViewSet

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
        return obj == request.user


class ConstellationViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    A viewset that provides read only functionality for the Constellation model.

    All other actions(create, update, destroy, etc.) are going to be available
    to superusers only through the admin panel.
    """

    serializer_class = ConstellationSerializer
    permit_list_expands = ['galaxies']

    def get_queryset(self):
        queryset = Constellation.objects.all()

        if is_expanded(self.request, 'galaxies'):
            queryset = queryset.prefetch_related('galaxies')

        return queryset


class ConstellationImageViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    A viewset that provides read only functionality for the ConstellationImage model.

    All other actions(create, update, destroy, etc.) are going to be available
    to superusers only through the admin panel.
    """

    serializer_class = ConstellationImageSerializer
    queryset = ConstellationImage.objects.all()


class GalaxyViewSet(FlexFieldsModelViewSet):
    """
    A viewset for the Galaxy model.

    It provides full functionality for the authenticated owner of the object,
    and read-only options for all other users - authenticated or not.
    """

    serializer_class = GalaxySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOfObjectOrReadOnly,)
    permit_list_expands = ['images']

    def get_queryset(self):
        queryset = Galaxy.objects.all()

        if is_expanded(self.request, 'images'):
            queryset = queryset.prefetch_related('images')

        return queryset

    def perform_create(self, serializer):
        """
        Prevents an authenticated user creating a record with the id of another user.
        """
        serializer.save(owner=self.request.user)


class GalaxyImageViewSet(FlexFieldsModelViewSet):
    """
    A viewset for the GalaxyImage model.

    It provides full functionality for the authenticated owner of the object,
    and read-only options for all other users - authenticated or not.
    """

    serializer_class = GalaxyImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOfObjectOrReadOnly,)
    queryset = GalaxyImage.objects.all()

    def perform_create(self, serializer):
        """
        Prevents an authenticated user creating a record with the id of another user.
        """
        serializer.save(owner=self.request.user)


class PostViewSet(FlexFieldsModelViewSet):
    """
    A viewset for the Post model.

    It provides full functionality for the authenticated owner of the object,
    and read-only options for all other users - authenticated or not.
    """

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOfObjectOrReadOnly,)
    permit_list_expands = ['images']

    def get_queryset(self):
        queryset = Post.objects.all()

        if is_expanded(self.request, 'images'):
            queryset = queryset.prefetch_related('images')

        if is_expanded(self.request, 'comments'):
            queryset = queryset.prefetch_related('comments')

        return queryset

    def perform_create(self, serializer):
        """
        Prevents an authenticated user creating a record with the id of another user.
        """
        serializer.save(owner=self.request.user)


class PostImageViewSet(FlexFieldsModelViewSet):
    """
    A viewset for the PostImage model.

    It provides full functionality for the authenticated owner of the object,
    and read-only options for all other users - authenticated or not.
    """

    serializer_class = PostImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOfObjectOrReadOnly,)
    queryset = PostImage.objects.all()

    def perform_create(self, serializer):
        """
        Prevents an authenticated user creating a record with the id of another user.
        """
        serializer.save(owner=self.request.user)


class CommentViewSet(FlexFieldsModelViewSet):
    """
    A viewset for the Comment model.

    It provides full functionality for the authenticated owner of the object,
    and read-only options for all other users - authenticated or not.
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOfObjectOrReadOnly,)
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        """
        Prevents an authenticated user creating a record with the id of another user.
        """
        serializer.save(owner=self.request.user)
