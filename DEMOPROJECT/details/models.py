from django.db import models


# Create your models here.
class Companydetails(models.Model):
    CompanyName = models.CharField(primary_key=True, max_length=100, default=None)
    GST = models.CharField(null=True, max_length=100, default=None)

class ProductDetails(models.Model):
    ProductName = models.CharField(primary_key=True, max_length=100, default=None)
    CompanyName = models.ForeignKey(Companydetails,on_delete=models.CASCADE)
    Cost = models.FloatField(null=False,default=None)

class PurchaseDetails(models.Model):
    orderNo = models.CharField(null=True, max_length=100, default=None)
    CompanyName = models.ForeignKey(Companydetails,on_delete=models.CASCADE)
    ProductName = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    Quantity = models.FloatField(null=False,default=None)
    Rate = models.FloatField(null=False,default=None)
    Total = models.FloatField(null=False,default=None)

