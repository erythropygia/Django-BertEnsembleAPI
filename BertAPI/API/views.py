from django.shortcuts import render,redirect

#LOGIN-REQUESTS
#####################################################################################################################

from django.contrib.auth.decorators import login_required
@login_required(login_url='/')
def user_details(request):
    user = request.user
    auth_token = user.auth_token.key if hasattr(user, 'auth_token') else None
    context = {'user': user , 'auth_token': auth_token}
    return render(request, 'userdetails.html', context)
#####################################################################################################################

#SIGN-UP-REQUESTS
#####################################################################################################################
from .forms import SignUpForm
from django.contrib.auth import login as auth_login
from rest_framework.authtoken.models import Token

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = Token.objects.get(user=user)
            # Kullanıcının kaydedildiği sayfaya yönlendirme
            return redirect('/login')
    else:
        form = SignUpForm()
    return render(request, 'login.html', {'form': form})
#####################################################################################################################


#APIREQUESTS
#####################################################################################################################
#BertModelRequest
from django.http import JsonResponse
import BertAPI.API.functions as BertFunctions

#API-KEY
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def process_text(request):
    if request.user.is_authenticated:
        text = request.GET.get('text', '') 
        if text == '':
            result = "Text parameter is null."
        else: 
            print(text)
            result = BertFunctions.predict(text)
        
        return Response({'text':BertFunctions.decode_url(text),'result': result}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)


#####################################################################################################################


   