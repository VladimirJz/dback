#from django import forms
from app.catalog.models import Servers
import floppyforms as forms
import floppyforms.__future__ as forms
from floppyforms import widgets

class NewServerForm(forms.ModelForm):

     class Meta:
        model = Servers
        fields = ('__all__')

     #    fields=('Server','Host','Instance',)
     #    widgets={'Server':widgets.TextInput(),
     #             'Host':widgets.TextInput(),
     #             'Instance':widgets.TextInput(),}
    
    
    # works fin on as_p
     # class Meta:
     #    model = Servers
     #     #fields = ('__all__')
     #    fields=('Server','Host','Instance',)
     #    widgets={'Server':widgets.TextInput(),
     #             #'Server':widgets.TextInput(attrs={'class':'form-control','placeholder': 'Identificador del servidor'}),
     #             'Host':widgets.TextInput(),
     #             'Instance':widgets.TextInput(),}
            
         


##-- test
     #    comment = forms.CharField(
     #        widget=forms.TextInput(attrs={'size':'40'}))

    # class Meta:
    #     model = Servers
    #     fields = ('__all__')
    # def __init__(self, *args, **kwargs):
    #     super(NewServerForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         self.fields[field_name].widget.attrs['placeholder'] = field.label