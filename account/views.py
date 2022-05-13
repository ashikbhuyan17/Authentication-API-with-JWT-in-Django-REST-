from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from yaml import serialize
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from django.contrib.auth import authenticate

# Create your views here.

class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        print("/////////////////////",serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        

class   UserLoginView(APIView):
    def post(self, request, format=None):
        serialize = UserLoginSerializer(data=request.data) 
        if serialize.is_valid(raise_exception=True):
            email = serialize.data.get('email')
            pasword = serialize.data.get('password')
            user = authenticate(email=email, password=pasword)
            if user:
                return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
            return Response({'errors':{'non_field_errors':['Email or password is not valid']}}, 
            status=status.HTTP_404_NOT_FOUND)    
