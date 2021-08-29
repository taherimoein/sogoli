from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from main.serializer import master_data
from django.http import JsonResponse
from main.views import base_fuction
from django.utils import timezone
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
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
def is_not_authenticated(request):
    return JsonResponse({'message' : 'You are not authenticated.'}, status = HTTP_401_UNAUTHORIZED)

@csrf_exempt
@require_POST
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
@require_POST
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
            if User.objects.filter(mobile = mobile_number).exists():
                register_status = True
                # login user
                this_user = User.objects.get(mobile = mobile_number)
                login(request, this_user)

                return JsonResponse({'message' : 'user is login', 'register': register_status, 'id': this_user.id} , status = HTTP_200_OK)
            else:
                return JsonResponse({'message' : 'user is not register', 'register': register_status, 'id': this_user.id} , status = HTTP_200_OK)
        else:
            return JsonResponse({'message' : 'the code or mobile number entered is incorrect.'} , status = HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_POST
@login_required(login_url = 'api:is_not_authenticated_api')
def signout(request):
    try:
        logout(request)
        return JsonResponse({'message' : 'user is logout'}, status = HTTP_200_OK, safe = False)
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
@require_POST
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
        login(request, this_user)

        return JsonResponse({'message' : 'user is login', 'id': this_user.id} , status = HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_POST
@login_required(login_url = 'api:is_not_authenticated_api')
def user_details(request):
    try:
        # get data
        user_id = request.POST.get('id')
        if User.objects.filter(id = user_id).exists():
            this_user = User.objects.get(id = user_id)
            serializer = master_data.UserDetailsSerializer(this_user)
            return JsonResponse(serializer.data, status = HTTP_200_OK, safe = False)
        else:
            return JsonResponse({'message': 'There is no user with this ID in the system.'}, status = HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)
