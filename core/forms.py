from django import forms
from .models import Seminar

class NewSeminarForm(forms.ModelForm):

    class Meta:
        model = Seminar
        exclude = ['teacher', 'participants', 'is_deleted']
        widgets = {
            "title": forms.TextInput(attrs={"class":"form-control"}),
            "description": forms.Textarea(attrs={"class":"form-control", "rows":4}),
            "price": forms.NumberInput(attrs={"class":"form-control"}),
            "location": forms.Textarea(attrs={"class":"form-control", "rows":4}),
            "is_public": forms.CheckboxInput(attrs={"class":"form-check-input"}),
            "is_inperson": forms.CheckboxInput(attrs={"class":"form-check-input"}),
            "session_start": forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            "session_end": forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            # "session_date": forms.DateInput(attrs={"class":"form-control", "type":"date"}, format="%Y-%m-%d"),
            # "session_time_start": forms.TimeInput(attrs={"class":"form-control", "type":"time"}),
            # "session_time_end": forms.TimeInput(attrs={"class":"form-control", "type":"time"}),
            "image": forms.FileInput(attrs={"class":"form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            for name in self.fields:
                if self.errors.get(name):
                    current_class = self.fields[name].widget.attrs.get("class", "")
                    self.fields[name].widget.attrs["class"] = (f"{current_class} is-invalid").strip()

    def clean(self):
        data = super().clean()
        session_start = data.get('session_start')
        session_end = data.get('session_end')
        if session_end <= session_start:
            self.add_error('session_start', '')
            self.add_error('session_end', 'session end must be greater than session start.')
        return data