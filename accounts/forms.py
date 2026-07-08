from django import forms
from .models import User

# class RegisterForm(forms.Form):
#     firstname=forms.CharField(
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Your name'
#         })
#         )

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "phone", "email", "address", "country", "city", "profile_picture"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            # field.widget.attrs['required'] = ''
    widgets = {
        "country": forms.Select(attrs={"class": "form-select"}),
        'city': forms.TextInput(attrs={'class': 'form-select'}),
    }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not phone.isdigit():
            raise forms.ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) != 11:
            raise forms.ValidationError(
                "Phone number must be exactly 11 digits."
            )

        return phone