from django.urls import path
from . import views
app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name="order_create"),
    path('history/', views.order_history, name="order_history"),
    path('payment/', views.payment_process, name="process"),
    path('success/', views.payment_done, name="done"),
    path('canceled/', views.payment_canceled, name="canceled"),
    path("admin/order/<int:order_id>/", views.admin_order_detail,
         name="admin_order_detail"),
    path("order/<int:order_id>/", views.order_detail,
         name="order_detail"),
    path("admin/order/<int:order_id>/pdf/", views.admin_order_pdf,
         name="admin_order_pdf"),
]
