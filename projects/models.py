from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    tech_stack = models.CharField(max_length=300, help_text="Comma separated technologies")
    github_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    created_date = models.DateField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('draft', 'Draft'),
            ('archived', 'Archived')
        ],
        default='active'
    )

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project-detail', args=[self.slug])

    def tech_list(self):
        return [tech.strip() for tech in self.tech_stack.split(',')]