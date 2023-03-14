from django.shortcuts import render,redirect

#USER-DETAILS-REQUESTS
#####################################################################################################################
from .admin import AdminPanel
from django.contrib.auth.decorators import login_required
@login_required(login_url='/login')
def user_details(request):
    user = request.user
    #auth_token = user.auth_token.key if hasattr(user, 'auth_token') else None
    auth_token = AdminPanel.token(user,user)
    phone = AdminPanel.phone(user,user)
    usage_limit = AdminPanel.usage_limit(user,user)
    usage_count = AdminPanel.usage_count(user,user)
    print(usage_count)
    context = {'user': user, 'auth_token': auth_token, 'phone': phone, 'usage_limit': usage_limit, 'usage_count': usage_count}
    return render(request, 'userdetails.html', context)
#####################################################################################################################

#SIGN-UP-REQUESTS
#####################################################################################################################
from .forms import SignUpForm
from django.contrib.auth import login as auth_login
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = Token.objects.get(user=user)
            messages.success(request, 'Success! Please log in and use Cer-NLP API!')
            return redirect('/login')
        else:
            errors = form.errors.as_data()
            for error_field, error_msgs in errors.items():
                if(len(errors)<2):
                    for error_msg in error_msgs:
                        if error_field == 'email':
                            messages.error(request, 'The email is already taken.')
                        elif error_field == 'username':
                            messages.error(request, 'The username is already taken.')
                        else:
                            messages.error(request, error_msg)
                else:
                    messages.error(request, 'Please check your informations.')
                    break
    else:
        form = SignUpForm()
    return render(request, 'login.html', {'form': form})

#####################################################################################################################


#REQUEST-CALCULATOR
#############################################################################
from rest_framework.throttling import UserRateThrottle

class UserThrottle(UserRateThrottle):
    scope = 'user'
#############################################################################


#APIREQUESTS
#####################################################################################################################
#BertModelRequest
from django.http import JsonResponse
import BertAPI.API.functions as BertFunctions

#API-KEY
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from .models import UserUsage

def check_usage_limit(request):
    now = datetime.now()
    month_start = datetime(now.year, now.month, 1)
    usage = UserUsage.objects.filter(user=request.user, created__gte=month_start).count()
    if usage >= AdminPanel.usage_limit(request.user,request.user):
        return False
    UserUsage.objects.create(user=request.user)
    return True

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
@throttle_classes([UserThrottle])
def process_text(request):
    if request.user.is_authenticated:
        if check_usage_limit(request):
            text = request.GET.get('text', '') 
            if text == '':
                result = "Text parameter is null."
            else: 
                result = BertFunctions.predict(text)
            return Response({'text':BertFunctions.decode_url(text),'result': result}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You have exceeded your monthly usage limit.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    else:
        return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

#####################################################################################################################

