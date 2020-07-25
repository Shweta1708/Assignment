from django.urls import path

from .views import *

urlpatterns = [
    path('AddCompany/', AddCompany.as_view()),
    path('AddProduct/', AddProduct.as_view()),
    path('AddOrder/', AddOrder.as_view()),
    path('ViewCompany/', ViewCompany.as_view()),
    path('ViewProducts/', ViewProducts.as_view()),
    path('ViewOrders/', ViewOrders.as_view()),
    ]