from django.shortcuts import render

# Create your views here.
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


   