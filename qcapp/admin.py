from django.contrib import admin

# Register your models here.
from .models import SimpleItem

admin.site.register(SimpleItem)
