from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Profile(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"))
    avatar = models.ImageField(_("Avatar"), upload_to='avatars/', null=True, blank=True)
    github = models.URLField(_("GitHub URL"), blank=True)
    linkedin = models.URLField(_("LinkedIn URL"), blank=True)
    email = models.EmailField(_("Email"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
        related_name='skills'
    )
    description = models.TextField(_("Description"), blank=True)
    icon = models.CharField(_("Icon"), max_length=50, blank=True, help_text="Lucide icon name")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Project(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    description = models.TextField(_("Description"))
    image = models.ImageField(_("Image"), upload_to='projects/', null=True, blank=True)
    technologies = models.ManyToManyField(Skill, related_name='projects')
    demo_url = models.URLField(_("Demo URL"), blank=True)
    github_url = models.URLField(_("GitHub URL"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    content = models.TextField(_("Content"))
    image = models.ImageField(_("Image"), upload_to='blog/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    message = models.TextField(_("Message"))
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(_("Is Read"), default=False)

    def __str__(self):
        return f"Message from {self.name}"
