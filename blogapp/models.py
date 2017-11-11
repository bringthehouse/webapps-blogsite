from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

# Create your models here.
class Articles(models.Model):
    slug_field = models.SlugField()
    title = models.CharField(max_length=100, blank=False)
    tags = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)

    author = models.ForeignKey(User)

    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    created = models.DateTimeField(default=datetime.now())
    updated = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ['-created']
