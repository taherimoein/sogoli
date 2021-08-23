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
import requests
# get model
from main.models import User, BeautyShop

# ----------------------------------------------------------------------------------------------------------------------------

@csrf_exempt
@require_GET
@login_required(login_url = 'api:is_not_authenticated_api')
def beautyshop_list(request):
    try:
        # get data
        beautyshops = BeautyShop.objects.filter(publish = True).order_by('-rate')
        serializer = master_data.BeautyShopSerializer(beautyshops, many = True)
        return JsonResponse(serializer.data, status = HTTP_200_OK, safe = False)
    except Exception as e:
        return JsonResponse({'message' : str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_POST
@login_required(login_url = 'api:is_not_authenticated_api')
def beautyshops_information_with_search(request):
    try:
        # get data
        this_search = request.POST.get('search')
        # set search regex
        this_search = this_search.split(' ')
        this_search = list(filter(lambda i: i != '', this_search))
        search_word_list = []
        for word in this_search:
            search_word = list(map(lambda x: x + '\s*', word.replace(' ','')[:-1]))
            search_word = ''.join(search_word) + word[-1]
            search_word_list.append(search_word)
        search_word = r'.*'.join(search_word_list)
        # search in title
        beautyshops = BeautyShop.objects.filter(title__regex = search_word, publish = True).order_by('-rate')
        serializer = master_data.BeautyShopSerializer(beautyshops, many = True)
        return JsonResponse(serializer.data, status = HTTP_200_OK, safe = False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@require_POST
@login_required(login_url = 'api:is_not_authenticated_api')
def beautyshop_details(request):
    try:
        # get data
        beautyshop_id = request.POST.get('id')
        # search in beautyshops
        if BeautyShop.objects.filter(id = beautyshop_id, publish = True).exists():
            this_beautyshop = BeautyShop.objects.get(id = beautyshop_id)
            beautyshop_serializer = master_data.BeautyShopDetailsSerializer(this_beautyshop)
            # get beautyshop post
            beautyshop_posts = this_beautyshop.post_beautyshop.filter(publish = True)
            post_serializer = master_data.PostSerializer(beautyshop_posts, many = True)
            return JsonResponse({'beautyshop': beautyshop_serializer.data, 'posts': post_serializer.data}, status = HTTP_200_OK, safe = False)
        else:
            return JsonResponse({'message': 'there is no beauty salon with this ID.'}, status = HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status = HTTP_500_INTERNAL_SERVER_ERROR)