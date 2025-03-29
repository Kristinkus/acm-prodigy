from django import forms

from volunteers.models import Volunteer


class VolunteerForm(forms.ModelForm):

    class Meta:
        model = Volunteer
        fields = (
            'lastname',
            'firstname',
            'secondname',
            'phone',
            'telegram',
            'email',
            'education',
            'tshirt_size',
            'group',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'