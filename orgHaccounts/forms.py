from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.files.images import get_image_dimensions
from .models import FileUpload, UserAvatar

User = get_user_model()
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label= 'Email address', widget=forms.TextInput(attrs={'class': 'form-control col-lg-6'}),)
    date_of_birth = forms.DateField(label= 'Birth Date', widget=forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'form-control col-lg-6',}),)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control col-lg-6'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control col-lg-6'}))

    class Meta:
        model = User
        fields = ['email','date_of_birth', 'password1', 'password2']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control col-lg-6'}),
            'date_of_birth': forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'form-control col-lg-6',}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email already exists!")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "The given  passwords do not match!")
        return cleaned_data
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserAvatar
        fields = ['avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'gif', 'png', 'jpg']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF, JPG or PNG image.')
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')
        except AttributeError:
            pass
        return avatar
class OHUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label= 'Email address', widget=forms.TextInput(attrs={'class': 'form-control col-lg-6', 'type':'text',}),)
    date_of_birth = forms.DateField(label= 'Birth Date', widget=forms.DateInput(format=('%d-%m-%Y'), attrs={'class':'form-control col-lg-6', 'type':'Date','value': '{ user_date_of_birth }'}),)
    
    class Meta:
        model=User
        fields=['email', 'date_of_birth']

class FileUploadForm(forms.ModelForm):
    file = forms.FileField(label= 'File', widget=forms.FileInput(attrs={'class': 'form-control col-lg-6', 'type':'file',}),)
    
    class Meta:
        model= FileUpload
        fields=['file']

class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [] 

class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control col-lg-6','type':'text','name': 'email'}), 
        label='Email address')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control col-lg-6','type':'password', 'name': 'password',}),
        label='Password')
    class Meta:
        model = User
        fields = ['email', 'password']

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'date_of_birth',]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1 != password2:
            self.add_error("password2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'date_of_birth', 'is_active', 'staff', 'admin']

    def clean_password(self):
        return self.initial["password"]