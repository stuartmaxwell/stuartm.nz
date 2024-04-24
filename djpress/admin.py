"""djpress admin configuration."""

from django.contrib import admin

# Register the models here.
from .models import Category, Content

admin.site.register(Category)
admin.site.register(Content)
