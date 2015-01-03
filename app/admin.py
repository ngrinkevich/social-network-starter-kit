# -*- coding: utf-8 -*-
import os, json, urllib, urllib2
from django import forms
from django.contrib.gis import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.files import File 

from app.models import User

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'display_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User

    def clean_password(self):
        return self.initial["password"]

    
class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'display_name', 'gender', 'avatar', 'avatar_ext', 'is_active', 'is_admin', 'is_staff')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('display_name', 'avatar', 'avatar_ext')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Activation', {'fields': ('is_active',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'display_name', 'gender', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


def import_random_user(request):
    
    gender = {'female': 1, 'male': 0}

    result = json.load(urllib2.urlopen('http://api.randomuser.me/'))['results'][0]['user']

    user = User(email=result['email'], 
        display_name="%s %s"%(result['name']['first'], result['name']['last']),
        gender=gender[result['gender']],
        date_joined = result['registered'],
        about = "Hello! My name is %s and I'm from %s, %s"%(result['name']['first'].title(), result['location']['city'].title(), result['location']['state'].title()),
        address = "%s, %s, %s, %s"%(result['location']['street'].title(), result['location']['city'].title(), result['location']['state'].title(), result['location']['zip'].title()),
        phone = result['phone'],
        avatar_ext = result['picture']['large'],
        is_active=True)
    
    #image = urllib.urlretrieve(result['picture']['large'])
    #user.avatar.save(os.path.basename(result['picture']['large']),File(open(image[0])))
    user.save()

    return HttpResponseRedirect(reverse('admin:app_user_changelist'))



import_random_user = staff_member_required(import_random_user)
