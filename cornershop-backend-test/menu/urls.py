from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views, viewsets

# Menu API router.
router = DefaultRouter()
router.register(r"menu-api", viewsets.MenuViewSet, basename="api-menu")

urlpatterns = [
    path("", include(router.urls)),
    path("menu/", views.menuList, name="menu-list"),
    path("menu/<uuid:pk>/", views.menuResponse, name="menu-response"),
    path("menu/<uuid:pk>/detail/", views.menuDetail, name="menu-detail"),
]
