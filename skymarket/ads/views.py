from ads.filters import AdFilter
from ads.models import Ad, Comment
from ads.serializers import AdSerializer, CommentSerializer, AdDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework import pagination, viewsets, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class AdPagination(pagination.PageNumberPagination):
    page_size = 4


class CommentPagination(pagination.PageNumberPagination):
    page_size = 10


# TODO view функции. Предлагаем Вам следующую структуру - но Вы всегда можете использовать свою
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    pagination_class = AdPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'me']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == 'me':
            return Ad.objects.filter(author=self.request.user).all()
        else:
            return Ad.objects.all()

    def get_serializer_class(self):
        if self.action == ('list', 'create', 'destroy', 'update'):
            return AdSerializer
        elif self.action == 'retrieve':
            return AdDetailSerializer

        return super().get_serializer_class()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        ad_instance = get_object_or_404(Ad, id=self.kwargs['ad_pk'])

        return ad_instance.comment_set.all()

    def perform_create(self, serializer):
        ad_instance = get_object_or_404(Ad, id=self.kwargs['ad_pk'])
        user = self.request.user
        serializer.save(author=user, ad=ad_instance)

