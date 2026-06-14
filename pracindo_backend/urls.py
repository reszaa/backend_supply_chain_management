from django.contrib import admin
from django.urls import path, include
from django.conf import settings             
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/purchase-order/', include('purchaseOrder.urls')),
    path('api/suplier/', include('suplier.urls')),
    path('api/customer/', include('customer.urls')),
    path('api/staff/', include('staffUser.urls')),
    path('api/belanja/', include('belanja.urls')),
    path('api/logistic/', include('logistic.urls')),
    path('api/stock-raw/', include('stock_raw.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)