from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=True, blank=True)
    email = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=32, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=128, null=True)

    def __str__(self) -> str:
        return str(self.id)

    @property
    def shipping(self):
        items = self.orderitem_set.all()
        for item in items:
            if item.product.digital == False:
                return True

        return False

    @property
    def get_total(self):
        items = self.orderitem_set.all()
        total = sum([item.get_total for item in items])

        return total

    @property
    def get_quantity(self):
        items = self.orderitem_set.all()
        total = sum([item.quantity for item in items])
        
        return total

class OrderItem(models.Model):

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity

class ShippingAddress(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    state = models.CharField(max_length=32, null=True, blank=True)
    zipcode = models.CharField(max_length=32, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)



