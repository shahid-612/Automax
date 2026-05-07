from django.db.models import CharField
from localflavor.pk import forms 


# changed this field as it is inbuilt syntax error in the package so it would also b reflected in production
class ModifiedPostCodeField(CharField):
    description = "Pakistani Postcode"
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 5
        super().__init__(*args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.PKPostalCodeField}
        defaults.update(kwargs)
        return super().formfield(**defaults)