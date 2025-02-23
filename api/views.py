from rest_framework import viewsets, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .models import Profile, Category, Skill, Project, BlogPost, Contact, Tag
from .serializers import (
    ProfileSerializer,
    CategorySerializer,
    SkillSerializer,
    ProjectSerializer,
    BlogPostSerializer,
    BlogPostCreateUpdateSerializer,
    ContactSerializer,
    TagSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all categories.

    retrieve:
    Return the given category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all tags.

    retrieve:
    Return the given tag.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return the profile information.

    retrieve:
    Return the profile details.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all skills grouped by category.

    retrieve:
    Return the given skill.
    """
    queryset = Skill.objects.select_related('category').all()
    serializer_class = SkillSerializer

    def list(self, request, *args, **kwargs):
        skills = self.get_queryset()
        categorized_skills = {}

        for skill in skills:
            category_name = skill.category.name
            if category_name not in categorized_skills:
                categorized_skills[category_name] = []
            categorized_skills[category_name].append(SkillSerializer(skill).data)

        return Response(categorized_skills)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all projects.

    retrieve:
    Return the given project.
    """
    queryset = Project.objects.prefetch_related('technologies').all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all blog posts.

    retrieve:
    Return the given blog post.
    """
    queryset = BlogPost.objects.prefetch_related('tags').order_by('-created_at')
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogPostCreateUpdateSerializer
        return BlogPostSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    create:
    Create a new contact message.

    list:
    Return a list of all contact messages (admin only).

    retrieve:
    Return the given contact message (admin only).
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Send a contact message",
        request_body=ContactSerializer,
        responses={
            201: ContactSerializer,
            400: 'Bad Request',
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]