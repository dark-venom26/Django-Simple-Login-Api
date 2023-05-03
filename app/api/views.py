from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

import json
import random
import string
from .models import User

# Create User Api
@csrf_exempt
def registerUser(request):
    # Retrieve user data from request
    if request.method == 'POST':
        userData = json.loads(request.body)
        username = userData.get('username')
        password = userData.get('password')
        mobile = userData.get('mobile')
        name = userData.get('name')
        address = userData.get('address')
        email = userData.get('email')
        

        # Validate user data
        if not username.isalpha():
            return JsonResponse({'error': 'Username should be alphanumeric'})  
        
        if not len(mobile) == 10:
            return JsonResponse({'error': 'Please enter a valid mobile number of 10 digits'})    

        if not is_valid_email(email):
            return JsonResponse({'error': 'Please enter a valid email'})    

        
        if not is_valid_password(password):
            return JsonResponse({'error': 'Password should contains alphnumeric and some special character'})    

        # Create and save user object
        user = User(username=username, password=password, mobile=mobile, name=name, address=address, email=email)
        user.save()

        # Send email with password details
        send_mail(
            "You've created you account successfully!",
            f'Your password is {password}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        # Return user ID
        return JsonResponse({'user_id': user.id})
        # return HttpResponse('404 - Not Found')
    
    else:
        return HttpResponse('404 - Not Found')

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def is_valid_password(password):
    return any(c.isalpha() for c in password) and any(c.isdigit() for c in password) and any(c.isascii() for c in password)


# Login Api
@csrf_exempt
def loginUser(request):
    # Retrieve user credentials from request
    if request.method == 'POST':
        userData = json.loads(request.body)
        username = userData.get('username')
        password = userData.get('password')

        # Validate user credentials against database
        try:
            user = User.objects.get(username=username, password=password)
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid username or password'})

    else:
        return HttpResponse('404 - Not Found')


# All users Api
def allUsers(request):
    # Retrieve all users from database
    users = User.objects.all()

    print(users)
    # Serialize users to JSON format
    serialized_users = serializers.serialize('json', users)

    # Return users in JSON format
    return JsonResponse(serialized_users, safe=False)