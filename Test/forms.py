from .models import User
from django import forms
from django.core.validators import validate_email


class TextSendForm(forms.Form):
    text = forms.CharField(min_length=1)


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']

    def clean(self):
        super(UserUpdateForm, self).clean()

        id = self.data.get('id')
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')

        print(id, name, email, sep=',')

        try:
            id = User.objects.get(id=self.data.get('id'))
        except User.DoesNotExist:
            self._errors['id'] = self.error_class(['id does not exist'])

        if len(name) > 200:
            self._errors['name'] = self.error_class(['Name is larger than 200 symbols'])

        try:
            validate_email(email)
        except validate_email.ValidationError:
            self._errors['email'] = self.error_class(['Email is not valid'])

        return self.cleaned_data
