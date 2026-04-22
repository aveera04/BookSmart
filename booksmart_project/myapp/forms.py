from django import forms
from django.contrib.auth import get_user_model

User=get_user_model()
class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control border-primary'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control border-primary'})
    )
    # password1=forms.CharField(widget=forms.PasswordInput)
    # password2=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['first_name', 'last_name', 'mobile', 'email']
        widgets={
            'first_name': forms.TextInput(attrs={'class': 'form-control border-primary'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control border-primary'}),
            'mobile':forms.NumberInput(attrs={'class': 'form-control border-primary'}),
            'email':forms.EmailInput(attrs={'class': 'form-control border-primary'})
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user




class LoginForm(forms.Form):
    email=forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control border-primary'})
    )
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control border-primary'})
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Enter mobile number'}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile', '').strip()
        if mobile and not mobile.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")
        if mobile and (len(mobile) < 10 or len(mobile) > 12):
            raise forms.ValidationError("Mobile number must be 10-12 digits.")
        return mobile


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter current password'}),
        label="Current Password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        label="Confirm New Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_pwd = cleaned_data.get('new_password')
        confirm_pwd = cleaned_data.get('confirm_password')

        if new_pwd and confirm_pwd and new_pwd != confirm_pwd:
            raise forms.ValidationError("New passwords do not match.")

        if new_pwd and len(new_pwd) < 6:
            raise forms.ValidationError("New password must be at least 6 characters long.")

        return cleaned_data