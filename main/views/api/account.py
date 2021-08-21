from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from main.serializer import master_data
from django.http import JsonResponse
from main.views import base_fuction
from django.utils import timezone
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
import requests
# get model
from main.models import User, Validation

# ----------------------------------------------------------------------------------------------------------------------------

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def send_verify_code(request):
    try:
        # get data
        mobile_number = request.POST.get('mobile')
        # check mobile number
        if not base_fuction.is_valid_mobile_number(mobile_number):
            return JsonResponse({'message' : 'mobile number is not valid'} , status = HTTP_400_BAD_REQUEST)
        if Validation.objects.filter(mobile = mobile_number).exists():
            this_validation = Validation.objects.get(mobile = mobile_number)
            this_validation.validation_code = base_fuction.generate_random_code(6)
            this_validation.save()
            # send sms
            send_sms_status, error = base_fuction.send_sms(mobile_number, this_validation.validation_code)
            if not send_sms_status:
                return JsonResponse({'message' : error} , status = HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            this_validation = Validation.objects.create(mobile = mobile_number)
            # send sms
            send_sms_status, error = base_fuction.send_sms(mobile_number, this_validation.validation_code)
            if not send_sms_status:
                return JsonResponse({'message' : error} , status = HTTP_500_INTERNAL_SERVER_ERROR)

        return JsonResponse({'message' : 'ok'} , status = HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def signin(request):
    try:
        # get data
        mobile_number = request.POST.get('mobile')
        validation_code = request.POST.get('validation_code')
        # check mobile number
        if not base_fuction.is_valid_mobile_number(mobile_number):
            return JsonResponse({'message' : 'mobile number is not valid'} , status = HTTP_400_BAD_REQUEST)
        # check validation code
        if Validation.objects.filter(mobile = mobile_number, validation_code = validation_code).exists():
            register_status = False
            access_token = None
            if User.objects.filter(mobile = mobile_number).exists():
                register_status = True
                # login user
                base_url = 'http://127.0.0.1:8000'
                url = base_url + '/oauth/token/'
                data = {"grant_type": "password", "client_id": "M1y371MdyrYAJ5zWE3B6xUhmO00PDuIY9uyHnIKX", "username": mobile_number, "password": mobile_number}
                response = requests.post(url, data = data)
                result = response.json()
                access_token = result['access_token']

                return JsonResponse({'message' : 'user is login', 'register': register_status, 'token': access_token} , status = HTTP_200_OK)
            else:
                return JsonResponse({'message' : 'user is not register', 'register': register_status, 'token': access_token} , status = HTTP_200_OK)
        else:
            return JsonResponse({'message' : 'the code or mobile number entered is incorrect.'} , status = HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


def check_signup_fields(mobile, first_name, last_name, email):
    if not base_fuction.is_valid_mobile_number(mobile):
        return False, 'mobile number is not valid'
    if User.objects.filter(mobile = mobile).exists():
        return False, 'a user is available with this mobile number.'
    if not base_fuction.check_str_length(first_name, 50):
        return False, 'first_name is not valid'
    if not base_fuction.check_str_length(last_name, 150):
        return False, 'last_name is not valid'
    if email is not None and email != '':
        if not base_fuction.is_valid_email(email):
            return False, 'email is not valid'

    return True, None


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    try:
        # get data
        user_mobile_number = request.POST.get('mobile')
        user_first_name = request.POST.get('first_name')
        user_last_name = request.POST.get('last_name')
        user_email = request.POST.get('email')
        try:
            user_profile = request.FILES['profile']
        except:
            user_profile = None
        # check data
        check_status, error = check_signup_fields(user_mobile_number, user_first_name, user_last_name, user_email)
        if not check_status:
            return JsonResponse({'message' : error} , status = HTTP_400_BAD_REQUEST)
        # create user
        this_user = User.objects.create_user(user_mobile_number)
        this_user.first_name = user_first_name
        this_user.last_name = user_last_name
        if user_email is not None and user_email != '':
            this_user.email = user_email
        if user_profile is not None:
            this_user.profile = user_profile
        this_user.save()
        # login user
        base_url = 'http://127.0.0.1:8000'
        url = base_url + '/oauth/token/'
        data = {"grant_type": "password", "client_id": "M1y371MdyrYAJ5zWE3B6xUhmO00PDuIY9uyHnIKX", "username": user_mobile_number, "password": user_mobile_number}
        response = requests.post(url, data = data)
        result = response.json()
        access_token = result['access_token']

        return JsonResponse({'message' : 'user is login', 'token': access_token} , status = HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_details(request):
    try:
        # get data
        user_id = request.POST.get('id')
        # search in users
        if User.objects.filter(id = user_id, active = True).exists():
            this_user = User.objects.get(id = user_id)
            serializer = master_data.UserDetailsSerializer(this_user)
            return JsonResponse(serializer.data, status = HTTP_200_OK, safe = False)
        else:
            return JsonResponse({'message': 'there is no user with this ID.'}, status = HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)
