from main.views.api import account, main, order
from django.urls import path

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

app_name = 'api'
urlpatterns = [
    # is_not_authenticated api
    path('is-not-authenticated/', account.is_not_authenticated, name = 'is_not_authenticated_api'),
    # account api
    path('send-verify-code/', account.send_verify_code, name = 'send_verify_code_api'),
    path('signin/', account.signin, name = 'signin_api'),
    path('signup/', account.signup, name = 'signup_api'),
    path('signout/', account.signout, name = 'signout_api'),
    path('user-details/', account.user_details, name = 'user_details_api'),
    # main api
    path('beautyshops/', main.beautyshop_list, name = 'beautyshops_api'),
    path('search-in-beautyshops/', main.beautyshops_information_with_search, name = 'beautyshops_information_with_search_api'),
    path('beautyshop-details/', main.beautyshop_details, name = 'beautyshop_details_api'),
    path('follow-beautyshop/', main.follow_beautyshop, name = 'follow_beautyshop_api'),
    # order api
    path('create-order/', order.create_order, name = 'create_order_api'),
    path('user-orders/', order.user_orders, name = 'user_orders_api'),
    path('beautyshop-orders/', order.beautyshop_orders, name = 'beautyshop_orders_api'),
]