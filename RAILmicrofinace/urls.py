from django.contrib import admin
from django.urls import path, include
from index_page.views import index_view
from auths.views import login_user, register
from dashboard.views import dashboard,  transfer, send_procced, withdraw, withdraw_msg, deposit
from django.conf import settings
from django.conf.urls.static import static

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
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
