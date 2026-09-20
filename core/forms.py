from django import forms
from core.models import Seminar, Review, Organization, OrganizationMembership
from accounts.models import User, OrganizationInvitation
from django.db.models import Q

class NewSeminarForm(forms.ModelForm):
    price = forms.CharField(help_text='Set the price to zero so your seminar can be viewed for Free.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # organization = forms.ChoiceField(choices=)
    class Meta:
        model = Seminar
        exclude = ['teacher', 'participants', 'is_deleted']
        widgets = {
            'organization': forms.Select(attrs={'class':'form-select'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':4}),
            'location': forms.Textarea(attrs={'class':'form-control', 'rows':4}),
            'max_participants': forms.NumberInput(attrs={'class':'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'is_inperson': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'session_start': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'session_end': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class':'form-control', 'id': 'image-input', 'accept': 'image/*'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['organization'].queryset = Organization.objects.filter(Q(owner=user) | Q(members=user)).distinct()

        if self.is_bound:
            for name in self.fields:
                if self.errors.get(name):
                    current_class = self.fields[name].widget.attrs.get('class', '')
                    self.fields[name].widget.attrs['class'] = (f'{current_class} is-invalid').strip()

    def clean(self):
        data = super().clean()
        session_start = data.get('session_start')
        session_end = data.get('session_end')
        if session_start and session_end and session_end <= session_start:
            self.add_error('session_start', '')
            self.add_error('session_end', 'session end must be greater than session start.')
        return data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class':'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your review...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            for name in self.fields:
                if self.errors.get(name):
                    current_class = self.fields[name].widget.attrs.get('class', '')
                    self.fields[name].widget.attrs['class'] = (f'{current_class} is-invalid').strip()

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating <= 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating

    def clean_comment(self):
        comment = self.cleaned_data['comment'].strip()
        if not comment:
            raise forms.ValidationError('Comment cannot be empty.')
        return comment

class NewOrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description', 'logo', 'website']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'id': 'logo-input', 'accept': 'image/*'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            for name in self.fields:
                if self.errors.get(name):
                    current_class = self.fields[name].widget.attrs.get('class', '')
                    self.fields[name].widget.attrs['class'] = (f'{current_class} is-invalid').strip()

class OrganizationInvitationForm(forms.Form):
    organization_id = forms.IntegerField(widget=forms.HiddenInput)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
    role = forms.ChoiceField(choices=OrganizationMembership.Role.choices, widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, request_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_user = request_user

        if self.is_bound:
            for name in self.fields:
                if self.errors.get(name):
                    current_class = self.fields[name].widget.attrs.get('class', '')
                    self.fields[name].widget.attrs['class'] = (f'{current_class} is-invalid').strip()

    def clean_organization_id(self):
        organization_id = self.cleaned_data['organization_id']

        try:
            return Organization.objects.get(id=organization_id, owner=self.request_user)
        except Organization.DoesNotExist:
            raise forms.ValidationError('You do not have permission to use this organization.')

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('The user does not exist.')

    def clean(self):
        cleaned_data = super().clean()

        organization = cleaned_data.get('organization_id')
        invited_user = cleaned_data.get('username')

        if not organization or not invited_user:
            return cleaned_data

        if organization.owner == invited_user:
            raise forms.ValidationError('You can not send invitation for yourself.')

        membership_exists = OrganizationMembership.objects.filter(
            organization=organization,
            user=invited_user,
        ).exists()

        if membership_exists:
            raise forms.ValidationError('This user is already a member of this organization.')

        pending_invitation = OrganizationInvitation.objects.filter(
            organization=organization,
            user=invited_user,
            status=OrganizationInvitation.StatusChoices.PENDING,
        ).exists()

        if pending_invitation:
            raise forms.ValidationError('This user already has a pending invitation.')

        return cleaned_data