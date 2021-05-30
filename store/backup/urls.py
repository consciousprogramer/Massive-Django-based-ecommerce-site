from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("view", views.product_view, name="product_view"),
    path("get_meta_data", views.get_meta_data, name="get_meta_data"),
    path('handle_product_search/',views.handle_product_search,name="handle_product_search"),
    path('view/<str:ptype>/<int:p_id>/<int:v_id>',views.product_view,name='product_view'),
    path('view/<str:ptype>/<int:p_id>',views.product_view,name='product_view'),
    path("selected_variant/<int:p_id>/<int:v_id>", views.selected_variant, name="selected_variant"),
    path('handlecart/',views.handleCart,name='handlecart'),
    path('additemtocart/',views.addItemToCart,name='addItemToCart'),
    path('view/cart/',views.viewCart,name='viewcart'),
    path('orderpage/',views.orderpage,name='orderpage'),
    path('asyncsearch/',views.asyncsearch,name='asyncsearch'),
    path("handle_register/", views.handle_register, name="register"),
    path("handle_login/", views.handle_login, name="login"),
    path("handle_cart_convert/",views.handle_cart_convert,name="handle_cart_convert"),
    path("select-address/",views.select_address,name='select_address'),
    path('ps/',views.print_session,name='print_session'),
    path('select_payment_gateway/',views.select_payment_gateway,name='select_payment_gateway'),
    path('paytm_response/',views.paytm_response,name='paytm_response')
]
