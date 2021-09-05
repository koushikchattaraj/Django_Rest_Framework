from region.models import Region
from django.db import models
from django.template.defaultfilters import slugify


class Country(models.Model):
    region = models.ForeignKey(Region, related_name='region', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    country_code = models.CharField(max_length=30, null=True, blank=True)
    slug = models.SlugField()
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Country, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.name
