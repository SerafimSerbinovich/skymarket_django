from ads.views import AdViewSet, CommentViewSet
from django.urls import include, path
from rest_framework_nested import routers

# TODO настройка роутов для модели
ad_router = routers.SimpleRouter()
ad_router.register('ads', AdViewSet)

comment_router = routers.NestedSimpleRouter(ad_router, r'ads', lookup='ad')
comment_router.register('comments', CommentViewSet)

urlpatterns = [
    path("", include(ad_router.urls)),
    path("", include(comment_router.urls)),


]
