from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class SimpleItem(models.Model):
    name = models.CharField(max_length=1000)


# Createed model for Cell that physically belongs to the Cell Panel.
class Cell(models.Model):
    number = models.IntegerField(blank=False)
    type = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(blank=False, null=True)

    class Meta:
        unique_together = ('type', 'lot')


# Createed model for Cell-Panel.
class CellPanel(models.Model):
    type = models.CharField(max_length=100, blank=False)
    manufacturer = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(blank=False, null=True)
    sheet = models.BinaryField()
    cell = models.ForeignKey(Cell)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('type', 'manufacturer', 'lot')


# Createed model for Reagent.
class Reagent(models.Model):
    type = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(blank=False, null=True)
    manufacturer = models.CharField(max_length=100, blank=False)
    requiresIDcard = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('type', 'manufacturer', 'lot')


# Createed model for IDcard.
class IDcard(models.Model):
    type = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(blank=False, null=True)
    manufacturer = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('type', 'manufacturer', 'lot')


# Createed model for Control.
class Control(models.Model):
    type = models.CharField(max_length=1, choices=[('P', 'PK'), ('N', 'NK')])
    cell = models.ForeignKey(Cell)
    result = models.IntegerField(choices=[(0, '0'), (1, '+1'), (2, '+2'), (3, '+3'), (4, '+4')])
    created_at = models.DateTimeField(auto_now_add=True)


# Createed model for Essey specificity.
class Essey(models.Model):
    type = models.CharField(max_length=100, blank=False)
    reagent = models.ForeignKey(Reagent)
    control = models.ForeignKey(Control)
    technician = models.ForeignKey(User)
    doctor = models.ForeignKey(User)
    remark = models.CharField(max_length=200)
    consequence = models.CharField(max_length=1, choices=[('P', 'OK'), ('N', 'NOT OK')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('type', 'created_at', 'technician')
