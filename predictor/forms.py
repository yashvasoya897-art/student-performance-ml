from django import forms
from .models import Profile
from .forms import ProfileImageForm

class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = ["image"]
