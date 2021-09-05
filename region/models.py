from django.db import models
from django.template.defaultfilters import lower, slugify

class Region(models.Model):
    name = models.CharField(max_length=30, default="", unique=True)
    slug = models.SlugField()
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.name = self.name.lower()
        return super(Region, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name.title()
