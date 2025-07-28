from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('<int:pk>/', views.orderView, name='order'),
    path('<int:pk>/shipping', views.shippingView, name='shipping'),
    path('<int:pk>/checkout', views.paymentsView, name='checkout'),
    path('<int:pk>/success', views.successView, name='success')
]

