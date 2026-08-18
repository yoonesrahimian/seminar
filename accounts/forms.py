from django import forms
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "phone", "email", "address", "country", "city", "profile_picture"]
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off'}),
            'password': forms.PasswordInput(attrs={'id': 'password', 'autocomplete': 'off'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if self.is_bound:
            for name, field in self.fields.items():
                if self.errors.get(name):
                    field.widget.attrs['class'] += ' is-invalid'
        

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

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "phone", "email", "address", "country", "city", "profile_picture"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if self.is_bound:
            for name, field in self.fields.items():
                if self.errors.get(name):
                    field.widget.attrs['class'] += ' is-invalid'
        

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

# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField()

#     def clean(self):
#         data = super().clean()
#         username = data.get('username')
#         password = data.get('password')
#         user = authenticate(request, username=username, password=password)

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control form-control-lg"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-lg"})
    )