"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include

from app import views

app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("home/<int:page>/", views.next_page, name="next_page"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("product/<int:pk>/", views.view_product, name="product"),
    path("product/add_product/", views.add_product, name="add_product"),
    path("orders/", views.orders, name="orders"),
    path("orders/<int:pk>/", views.make_order, name="make_order"),
]
