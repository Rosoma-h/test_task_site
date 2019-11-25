from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import ProfileUser
from .models import user_registrated


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    # date_of_birth = forms.DateField(label='Дата рождения')

    # years_to_display = range(datetime.datetime.now().year - 100,
    #                          datetime.datetime.now().year)
    # birthdate = forms.DateField(label='Дата рождения',
    #             widget=forms.SelectDateWidget(years=years_to_display))

    class Meta:
        model = ProfileUser
        fields = ('username', 'email', 'first_name', 'last_name',
                  'date_of_birth', 'send_messages')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                help_text=password_validation.password_validators_help_text_html())

    password2 = forms.CharField(label='Пароль (повторно)',
                                widget=forms.PasswordInput,
                help_text='Введите тот же самый пароль еще раз для проверки')

    # date_of_birth = forms.DateField(label='Дата рождения')

    # years_to_display = range(datetime.datetime.now().year - 100,
    #                          datetime.datetime.now().year)
    # birthdate = forms.DateField(label='Дата рождения')
    # birthdate = forms.DateField(label='Дата рождения',
    #             widget=forms.SelectDateWidget(years=years_to_display))

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                      'Введенные пароли не совпадают',
                      code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = ProfileUser
        fields = ('username', 'email', 'password1', 'password2',
                  'first_name', 'last_name', 'date_of_birth', 'send_messages')
