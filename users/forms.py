from django import forms
from .models import Users

class ExistingUserRegisterForm(forms.ModelForm):

    username = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'placeholder': 'Введіть логін'})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'test@gmail.com'})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )

    class Meta:
        model = Users
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Users.objects.filter(username=username).exists():
            raise forms.ValidationError('Користувач з таким логіном вже існує!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError('Користувач з такою поштою вже існує!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Паролі не збігаються!')
        return cleaned_data