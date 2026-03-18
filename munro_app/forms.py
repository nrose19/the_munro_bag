from django import forms
from django.contrib.auth.models import User
from munro_app.models import UserProfile, ClimbRecord, Munro
from django.db import models

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("passwords do not match")

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        required=False
    )
    
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'date_of_birth')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ClimbRecordForm(forms.ModelForm):
    climb_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    photos = forms.FileField(widget=MultipleFileInput(attrs={'multiple': True}), required=False)
    
    # Custom fields for time
    time_hr = forms.IntegerField(min_value=0, required=True, label="Total time (hr)")
    time_min = forms.IntegerField(min_value=0, max_value=59, required=True, label="Total time (min)")
    
    # Custom field for favourite
    is_favourite = forms.ChoiceField(
        choices=[('yes', 'yes'), ('no', 'no')],
        widget=forms.RadioSelect(),
        required=True,
        label="Is this your new favourite?"
    )

    star_rating = forms.ChoiceField(
        choices=[(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')],
        widget=forms.RadioSelect()
    )
    
    class Meta:
        model = ClimbRecord
        fields = ('munro', 'climb_date', 'total_meters_climbed', 
                  'total_distance', 'star_rating', 'comments')
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
        }
