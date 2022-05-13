from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from yaml import serialize
from .serializers import UserProfileSerializer, UserRegistrationSerializer,UserLoginSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.

# token generate manually
def get_tokens_for_user(user):
    print("user",user)
    refresh = RefreshToken.for_user(user)
    print("refresh token:",refresh)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
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
                token = get_tokens_for_user(user)
                return Response({'token':token,'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not valid']}}, 
                status=status.HTTP_404_NOT_FOUND)  # If user is not found      
        return Response(serialize.errors,status=status.HTTP_404_NOT_FOUND)    
           
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(selt,request,format=None):
        serialize = UserProfileSerializer(request.user)
        return Response(serialize.data)