from main.views.api import account, main
from django.urls import path

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

app_name = 'api'
urlpatterns = [
    # account api
    path('send-verify-code/', account.send_verify_code, name = 'send_verify_code_api'),
    path('signin/', account.signin, name = 'signin_api'),
    path('signup/', account.signup, name = 'signup_api'),
    path('user-details/', account.user_details, name = 'user_details_api'),
    # main api
    path('beautyshops/', main.beautyshop_list, name = 'beautyshops_api'),
    path('search-in-beautyshops/', main.beautyshops_information_with_search, name = 'beautyshops_information_with_search_api'),
    path('beautyshop-details/', main.beautyshop_details, name = 'beautyshop_details_api'),
]