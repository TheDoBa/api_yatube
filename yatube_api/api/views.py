from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated


from api.serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer
)
from posts.models import Group, Post
from .permissions import IsAuthorOrReadOnly


# class IsAuthorOrReadOnly(permissions.BasePermission):
#     """Пользовательское разрешение только автору."""

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Post."""

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""

    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для модели Group - только на чтение."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
