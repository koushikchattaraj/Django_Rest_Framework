from django.db import models
from country.models import Country
from django.template.defaultfilters import slugify


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    pincode = models.CharField(max_length=30, null=True, blank=True)
    slug = models.SlugField()
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(State, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name



