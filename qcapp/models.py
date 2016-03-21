from django.db import models
from django.contrib.auth.models import User


# Createed model for Cell that physically belongs to the Cell Panel.
class Cell(models.Model):
    number = models.IntegerField()
    type = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('type', 'lot')


# Createed model for Cell-Panel.
class CellPanel(models.Model):
    type = models.CharField(max_length=100, blank=False)
    manufacturer = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(null=True)
    sheet = models.BinaryField()
    cell = models.ForeignKey(Cell)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('type', 'manufacturer', 'lot')


# Createed model for Reagent.
class Reagent(models.Model):
    type = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(null=True)
    manufacturer = models.CharField(max_length=100, blank=False)
    requiresIDcard = models.BooleanField(default=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('type', 'manufacturer', 'lot')


# Createed model for IDcard.
class IDcard(models.Model):
    type = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(null=True)
    manufacturer = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('type', 'manufacturer', 'lot')


# Createed model for Control.
class Control(models.Model):
    type = models.CharField(max_length=1, choices=[('P', 'PK'), ('N', 'NK')], blank=False)
    cell = models.ForeignKey(Cell)
    result = models.IntegerField(choices=[(0, '0'), (1, '+1'), (2, '+2'), (3, '+3'), (4, '+4')], blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


# Createed model for Essey specificity.
class Essey(models.Model):
    type = models.CharField(max_length=100, blank=False)
    reagent = models.ForeignKey(Reagent)
    control = models.ForeignKey(Control)
    technician = models.ForeignKey(User, related_name='esseys_as_technician')
    doctor = models.ForeignKey(User, related_name='esseys_as_doctor')
    remark = models.CharField(max_length=200)
    consequence = models.CharField(max_length=1, choices=[('P', 'OK'), ('N', 'NOT OK')], blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('type', 'created_at', 'technician')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    roles = models.CharField(max_length=1, choices=[('T', 'Technician'), ('D', 'Doctor'), ('A', 'Admin')])
