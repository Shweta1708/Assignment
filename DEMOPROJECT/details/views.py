import json
import re
from datetime import datetime

from django.forms import model_to_dict
from django.shortcuts import render
import pandas as pd
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *


class AddCompany(APIView):
    def post(self, request):
        try:
            Companydetails.objects.create(CompanyName=request.data['Name'], GST=request.data['GST'])
            return Response(({"status": "Successfully created"}), status=status.HTTP_201_CREATED)
        except:
            return Response(({"status": "Unable to add comapny"}), status=status.HTTP_404_NOT_FOUND)


class AddProduct(APIView):
    def post(self, request):
        try:
            name = request.data['Name']
            productexists = ProductDetails.objects.filter(ProductName=name)
            if productexists:
                return Response(({"status": "Product Already Exists!!"}), status=status.HTTP_404_NOT_FOUND)

            company = Companydetails.objects.only('CompanyName').get(CompanyName=request.data['Company'])
            ProductDetails.objects.create(ProductName=request.data['name'], CompanyName=company,
                                          Cost=request.data['Cost'])
            return Response(({"status": "Successfully created"}), status=status.HTTP_201_CREATED)
        except:
            return Response(({"status": "Unable to add product"}), status=status.HTTP_404_NOT_FOUND)


class AddOrder(APIView):
    def post(self, request):
        try:
            productname = request.data['productname']
            quantity = request.data['quantity']
            data = list(ProductDetails.objects.filter(ProductName=productname).values_list())
            rate = data[0][2]
            Totalprice = rate * float(quantity)
            currentYear = datetime.now().year

            count = PurchaseDetails.objects.all().count()
            if count != 0:
                latestdata1 = PurchaseDetails.objects.latest('orderNo')
                oi_dict = model_to_dict(latestdata1)
                latestdata = oi_dict['orderNo']
                orderNo1 = latestdata.rsplit('/', 1)[1]
                yeardata = latestdata.rsplit('/', 2)[1]
                if yeardata != currentYear:
                    number = 0
                else:
                    number = int(orderNo1) + 1
            else:
                number = 0
            orderNo = 'PO/' + str(currentYear) + '/' + str(number)
            company = Companydetails.objects.only('CompanyName').get(CompanyName=request.data['comp_name'])
            product = ProductDetails.objects.only('ProductName').get(ProductName=productname)
            PurchaseDetails.objects.create(orderNo=orderNo, CompanyName=company, ProductName=product, Quantity=quantity
                                           , Rate=rate, Total=Totalprice)
            return Response(({"status": "Successfully created"}), status=status.HTTP_201_CREATED)
        except:
            return Response(({"status": "Unable to add order details"}), status=status.HTTP_404_NOT_FOUND)


class ViewCompany(APIView):
    def get(self, request):
        try:
            companyDetails = Companydetails.objects.all().values_list()
            return Response(({"data": companyDetails}), status=status.HTTP_201_CREATED)
        except:
            return Response(({"status": "Something went wrong"}), status=status.HTTP_404_NOT_FOUND)


class ViewProducts(APIView):
    def get(self, request):
        try:
            productDetails = ProductDetails.objects.all().values_list()
            return Response(({"data": productDetails}), status=status.HTTP_201_CREATED)
        except:
            return Response(({"status": "Something went wrong"}), status=status.HTTP_404_NOT_FOUND)


class ViewOrders(APIView):
    def get(self, request):
        try:
            pur_Details = PurchaseDetails.objects.all().values_list()
            return Response(({"data": pur_Details}), status=status.HTTP_201_CREATED)
        except:
            return Response(({"status": "Something went wrong"}), status=status.HTTP_404_NOT_FOUND)
