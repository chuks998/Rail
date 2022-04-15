"""RAILmicrofinace URL Configuration

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
from django.contrib import admin
from django.urls import path
from index_page.views import index_view
from auths.views import login_user, register
from dashboard.views import dashboard,  transfer, send_procced, withdraw, withdraw_msg, deposit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    # path('dashboard/', ProfileView.as_view(), name='dashboard'),
    path('transfer_funds/', transfer, name='transfer'),
    path('send_proceed/', send_procced, name='send_proceed'),
    path('withdraw_funds/', withdraw, name='withdraw'),
    path('withdraw_proceed', withdraw_msg, name='withdraw_msg'),
    path('deposit/', deposit, name='deposit'),
]
