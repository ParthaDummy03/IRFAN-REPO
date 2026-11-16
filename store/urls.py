from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart_page, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_cart_item, name="remove_cart_item"),
    path("outlets/", views.outlets, name="outlets"),
    path("outlets/select/<int:outlet_id>/", views.select_outlet, name="select_outlet"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_history, name="order_history"),
    path("orders/<str:order_number>/confirmed/", views.order_confirmed, name="order_confirmed"),
    path("orders/<str:order_number>/payment/", views.payment, name="payment"),
    path("orders/<str:order_number>/payment/save/", views.choose_payment, name="choose_payment"),
    path("signup/", views.signup, name="signup"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("offers/", views.offers, name="offers"),
    path("coupons/", views.coupons, name="coupons"),
    path("feedback/", views.feedback, name="feedback"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("opening-hours/", views.opening_hours, name="opening_hours"),
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("delivery/", views.delivery_dashboard, name="delivery_dashboard"),
]
