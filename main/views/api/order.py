from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
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
import json
# get model
from main.models import User, BeautyShop, Service, Order

# ----------------------------------------------------------------------------------------------------------------------------

@csrf_exempt
@require_POST
@login_required(login_url = 'api:is_not_authenticated_api')
def create_order(request):
    try:
        # get data
        user_id = request.POST.get('user_id')
        beautyshop_id = request.POST.get('beautyshop_id')
        services = json.loads(request.POST.get('services'))
        order_datetime = request.POST.get('order_datetime')
        payment_status = request.POST.get('payment_status')
        # create order
        user = User.objects.get(id = user_id)
        beautyshop = BeautyShop.objects.get(id = beautyshop_id)
        total_price = 0
        for item in services['list']:
            total_price += int(item['price'])
        order_status = True
        if payment_status == '0':
            order_status = True
        Order.objects.create(fk_user = user, fk_beautyshop =  beautyshop,\
            services = services, total_price = total_price, reservation_date = order_datetime,
            payment_status = order_status)
        # add order count
        user.orders_count += 1
        user.save()
        beautyshop.orders_count += 1
        beautyshop.save()
        return JsonResponse({'message' : 'ok'}, status = HTTP_201_CREATED)
    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_POST
@login_required(login_url = 'api:is_not_authenticated_api')
def user_orders(request):
    try:
        # get data
        user_id = request.POST.get('id')
        if User.objects.filter(id = user_id).exists():
            # get user orders
            orders = Order.objects.filter(fk_user = user_id).order_by('-reservation_date')
            serializer = master_data.UserOrderSerializer(orders, many = True)
            return JsonResponse(serializer.data, status = HTTP_200_OK, safe = False)
        else:
            return JsonResponse({'message': 'There is no user with this ID in the system.'}, status = HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_POST
@login_required(login_url = 'api:is_not_authenticated_api')
def beautyshop_orders(request):
    try:
        # get data
        beautyshop_id = request.POST.get('id')
        if BeautyShop.objects.filter(id = beautyshop_id).exists():
            # get beautyshop orders
            orders = Order.objects.filter(fk_beautyshop = beautyshop_id).order_by('-reservation_date')
            serializer = master_data.BeautyShopOrderSerializer(orders, many = True)
            return JsonResponse(serializer.data, status = HTTP_200_OK, safe = False)
        else:
            return JsonResponse({'message': 'There is no beautyshop with this ID in the system.'}, status = HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)