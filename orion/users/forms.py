from django import forms
from users.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'birth_year', 'bio', 'avatar']
        widgets = {
            'birth_year': DateInput,
        }
