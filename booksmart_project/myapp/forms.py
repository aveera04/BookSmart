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
    