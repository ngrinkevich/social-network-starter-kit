# -*- coding: utf-8 -*-
from django.contrib import messages
from app.models import User

def create_user(strategy, details, response, uid, user=None, *args, **kwargs):

    if user:
        messages.success(strategy.request, 'You have been successfully logged in.')  
        return
    else:
        messages.success(strategy.request, 'You have successfully registered and logged in.')

    gender = {'female': 1, 'male': 0}    
    return {
        'is_new': True,
        'user': User.objects.create_user(email=details.get('email'), is_active = True, gender=gender[response['gender']], display_name = details.get('first_name'), username = details.get('username'))
    }















