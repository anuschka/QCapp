from django.contrib import admin

# Register your models here.
from .models import Cell, Reagent, IdCard

admin.site.register(Cell)
admin.site.register(Reagent)
admin.site.register(IdCard)
