# groups
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import GroupViewSet, PublicGroupViewSet, PublicGroupDetailAPIView

router = DefaultRouter()
router.register(r'admin/groups', GroupViewSet, basename='admin-groups')
router.register(r'groups', PublicGroupViewSet, basename='public-groups')

urlpatterns = router.urls + [
    path('groups/slug/<slug:slug>/', PublicGroupDetailAPIView.as_view({'get': 'retrieve'})),
]
