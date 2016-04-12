from django.contrib import admin

# Register your models here.
from .models import Cell, Reagent, IdCard, CellPanel, UserProfile

admin.site.register(Cell)
admin.site.register(Reagent)
admin.site.register(IdCard)
admin.site.register(CellPanel)
admin.site.register(UserProfile)
