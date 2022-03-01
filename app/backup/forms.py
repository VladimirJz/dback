#from django import forms
from app.backup.models import Backups,Locations,Status

import floppyforms as forms
import floppyforms.__future__ as forms
from floppyforms import widgets


class BackupForm(forms.ModelForm):

     class Meta:
        model = Backups
        fields = ('__all__')

class LocationForm2(forms.ModelChoiceField ):
    class Meta:
        model=Locations
        fields=('__all__')

class UpdateLostForm(forms.Form):
    location=forms.ModelChoiceField(queryset=Locations.objects.filter(id__lt=4))
    status=forms.ModelChoiceField(queryset=Status.objects.all())


class BackupFormBulk(forms.ModelForm):
    pass