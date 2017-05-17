from django.db import models
from django.contrib.auth.models import User


# Createed model for Cell-Panel.
class CellPanel(models.Model):
    type = models.CharField(max_length=100, blank=False)
    manufacturer = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(null=True)
    # Sheet is a PDF file that the user uploads. Media file handing!
    sheet = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('type', 'manufacturer', 'lot')

    def __str__(self):
        return "My CellPanel type %s" % (self.type)


# Createed model for Cell. One Cell always belongs to only one CellPanel.
class Cell(models.Model):
    number = models.IntegerField()
    type = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    cell_panel = models.ForeignKey(CellPanel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('number', 'cell_panel')

    def __str__(self):
        return "My cell number %s in %s" % (self.number, self.type)


# Createed model for Reagent.
class Reagent(models.Model):
    type = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False, help_text='Lot number')
    expiry = models.DateField(null=True)
    manufacturer = models.CharField(max_length=100, blank=False)
    requiresIDcard = models.BooleanField(default=False, blank=False,
                                         help_text='Require ID card')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('type', 'manufacturer', 'lot')

    def __str__(self):
        return "Reagent %s by %s" % (self.type, self.manufacturer)


# Createed model for IDcard.
class IdCard(models.Model):
    type = models.CharField(max_length=100, blank=False)
    lot = models.CharField(max_length=100, blank=False)
    expiry = models.DateTimeField(null=True)
    manufacturer = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('type', 'manufacturer', 'lot')


# Createed model for Essey specificity.
class Essey(models.Model):
    type = models.CharField(max_length=100, blank=False)
    reagent = models.ForeignKey(Reagent, related_name='reagent_essey')
    idcard = models.ForeignKey(IdCard, null=True, related_name='idcard_essey')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('type', 'created_at')

# Created model for Control.
class Control(models.Model):
    type = models.CharField(max_length=1, choices=[('P', 'PK'), ('N', 'NK')], blank=False)
    cell = models.ForeignKey(Cell)
    result = models.IntegerField(choices=[(0, '0'), (1, '+1'), (2, '+2'), (3, '+3'), (4, '+4')], blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    essey = models.ForeignKey(Essey, related_name='essey_control')


# Created model for VAlidation.
class Validation(models.Model):
    technician = models.ForeignKey(User, related_name='technician')
    doctor = models.ForeignKey(User, related_name='doctor')
    remark = models.CharField(max_length=200, null=True)
    consequence = models.CharField(max_length=1, choices=[('P', 'OK'), ('N', 'NOT OK')], blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    essey = models.ForeignKey(Essey, related_name='essey_validation')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    roles = models.CharField(max_length=1, choices=[('T', 'Technician'), ('D', 'Doctor'), ('A', 'Admin')])
