from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileViewSet,
    CategoryViewSet,
    SkillViewSet,
    ProjectViewSet,
    BlogPostViewSet,
    ContactViewSet,
    TagViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'blog', BlogPostViewSet)
router.register(r'contact', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
