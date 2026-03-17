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
    # star_rating = models.IntegerField(choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])

    star_rating = forms.ChoiceField(
        choices=[(i,i) for i in range(1,6)],
        widget=forms.RadioSelect()
    )
    
    class Meta:
        model = ClimbRecord
        fields = ('munro', 'climb_date', 'total_meters_climbed', 
                  'total_distance', 'completion_time_hours', 
                  'star_rating', 'comments')
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
            # 'star_rating': forms.RadioSelect() \
        }
