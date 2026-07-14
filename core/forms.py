from django import forms
from .models import Seminar

class NewSeminarForm(forms.ModelForm):
    class Meta:
        model = Seminar
        exclude = ["teacher", "participants"]
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class":"form-control", "rows":4}),
            "price": forms.NumberInput(attrs={"class":"form-control"}),
            "location": forms.Textarea(attrs={"class":"form-control", "rows":4}),
            "is_public": forms.CheckboxInput(attrs={"class":"form-check-input"}),
            "is_inperson": forms.CheckboxInput(attrs={"class":"form-check-input"}),
            "session_date": forms.DateInput(attrs={"class":"form-control", "type":"date"}, format="%Y-%m-%d"),
            "session_time_start": forms.TimeInput(attrs={"class":"form-control", "type":"time"}),
            "session_time_end": forms.TimeInput(attrs={"class":"form-control", "type":"time"}),
            "image": forms.FileInput(attrs={"class":"form-control"}),
        }