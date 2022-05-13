from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from yaml import serialize
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
# Create your views here.

class RegisterView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serialize = UserLoginSerializer(data=request.data) 
        if serialize.is_valid(raise_exception=True):
            email = serialize.data.get('email')
            pasword = serialize.data.get('password')
            user = authenticate(email=email, password=pasword)
            if user:
                return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not valid']}}, 
                status=status.HTTP_404_NOT_FOUND)  # If user is not found      
        return Response(serialize.errors,status=status.HTTP_404_NOT_FOUND)    
           
