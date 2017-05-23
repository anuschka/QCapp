from django.contrib import admin

# Register your models here.
from .models import Cell, Reagent, IdCard, CellPanel, UserProfile, Essey, Control

admin.site.register(Reagent)
admin.site.register(IdCard)
admin.site.register(UserProfile, list_display=['user', 'roles'])
admin.site.register(CellPanel)
admin.site.register(Cell)
admin.site.register(Essey)
admin.site.register(Control)
