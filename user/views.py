from django.shortcuts import render
from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import *
from rest_framework import status
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.conf import settings
from django.http import JsonResponse
import random
from rest_framework import status
import boto3



@permission_classes([AllowAny, ])
class HealthCheckAPI(APIView):

    def get(self, request, format=None):
        print('yessssss')
        return Response({"status": "success", "message": "Service Run Successfully"}, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):  
    def post(self,request):
        try:
            data= request.data
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            password = data.get('password')
            email = data.get('email')
            country_code = data.get('country_code')
            mobile_number = data.get('mobile_number')
            address = data.get('address')
            country_name = data.get('country_name')
            state_name = data.get('state_name')
            zipcode = data.get('zipcode')
            gender = data.get('gender')
            bio = data.get('bio')
            date_of_birth = data.get('date_of_birth')
            role_name = data.get('role_name', 'employee')

            
            if request.user.role.role_name in ["supervisor","admin"]:
                pass
            else:
                return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if Customuser.objects.filter(mobile_number=mobile_number).exists():
                return JsonResponse({'status': 'error', 'message': 'Mobile number already exists'},status=status.HTTP_400_BAD_REQUEST)                  
            transaction.set_autocommit(False)

            try:
                role = RoleMaster.objects.get(role_name=role_name)
            except RoleMaster.DoesNotExist:
                return Response({'status':'error','message':'Role does not exist'},status=status.HTTP_400_BAD_REQUEST)
                            
            user = Customuser(
                first_name=first_name,
                last_name=last_name,
                password=make_password(password),
                email=email,
                role=role,
                country_code=country_code,
                mobile_number=mobile_number,
                address=address,
                country_name=country_name,
                state_name=state_name,
                zipcode=zipcode,
                gender=gender,
                bio=bio,
                date_of_birth=date_of_birth,
            )

            user.save()
            transaction.commit()
            refresh = RefreshToken.for_user(user)
            token_data = {'access': str(refresh.access_token),}
            return Response({'status': 'success', 'message': f'{role_name} Registration successful', 'token': token_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            transaction.rollback()
            return Response({'status': 'error', 'message':f'Something went wrong! {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)



class RoleCreationAPIView(APIView):   
    def post(self, request):
        try:
            role_name = request.data.get('role')
            description = request.data.get('description')
            
            if request.user.role.role_name == "superadmin":
                pass
            else:
                return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'},status=status.HTTP_400_BAD_REQUEST)

            if not role_name:
                return Response({'status':'error','message': 'Role name is required'}, status=status.HTTP_400_BAD_REQUEST)
            transaction.set_autocommit(False)
            try:
                role = RoleMaster.objects.get(role_name=role_name)
                return Response({'status':'error','message': 'Role already exists'}, status=status.HTTP_400_BAD_REQUEST)
            except RoleMaster.DoesNotExist:
                role = RoleMaster.objects.create(role_name=role_name, description=description,created_by=request.user.id)
                transaction.commit()
                return Response({'status':'success','message': 'Role created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status":"error","message":f"Something went wrong! {str(e)}"},status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    def post(self, request):
        try:
            mobile_number = request.data.get('mobile_number')
            password = request.data.get('password')
            try:
                user = Customuser.objects.get(mobile_number=mobile_number)
            except Customuser.DoesNotExist:     
                return Response({'status': 'error', 'message': 'mobile number not found'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if not check_password(password, user.password):
                return Response({'status': 'error', 'message': 'Incorrect Password'}, status=status.HTTP_401_UNAUTHORIZED)
                
            if user.role.role_name != 'superadmin' and not user.is_approved:
                return Response({'status': 'error', 'message': 'user is not approved to login. Please contact the administrator.'}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': f'{user.role.role_name} Role Logged in Successfully',
                'token': str(refresh.access_token)},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message':f'Something went wrong! {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class UserApprovalAPIView(APIView):
    def put(self, request):
        mobile_number = request.data.get('mobile_number')
        try:
            user = Customuser.objects.get(mobile_number=mobile_number)
        except Customuser.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
       
        try:
            if not request.user.role.role_name in ['admin', 'superadmin']:
                return Response({'status': 'error', 'message': 'You are not authenticated to perform this action'}, status=status.HTTP_401_UNAUTHORIZED)

            user.is_approved = True
            user.save()
            return Response({'status': 'success', 'message': f'User {user.first_name} has been approved'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'error', 'message': f'Something went wrong! {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

