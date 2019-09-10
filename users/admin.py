from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from users.models import UserProfile

# Register your models here.
class UserProfileCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='password',widget = forms.PasswordInput)
    password1 = forms.CharField(label='Confirm Password',widget = forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('username','email','mobile','first_name','last_name')

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password did not match")
        return password2

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserProfileChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('username','email','mobile','first_name','last_name',)

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserProfileChangeForm
    add_form = UserProfileCreationForm

    list_display = ('username','first_name','last_name',)
    list_filter = ('is_admin',)
    search_fields = ('username',)
    ordering = ('first_name','last_name')
    filter_horizontal = ()

admin.site.register(UserProfile, UserAdmin)
