from itertools import product
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
from datetime import datetime
from .utils import cookieCart,cartData,guestOrder
# Create your views here.

def store(request):

     data = cartData(request)
     
     cartItems_quantity = data["cartItems"]
     
     products = Product.objects.all()

     context = {
          "products": products,
          "cartItems_quantity": cartItems_quantity,
     }
     return render(request, 'store/store.html', context)

def cart(request):

     data = cartData(request)
     
     cartItems_quantity = data["cartItems"]
     order = data["order"]
     items = data["items"]

     context = {
          "items": items,
          "order": order,
          "cartItems_quantity": cartItems_quantity
     }
     return render(request, 'store/cart.html', context)

def checkout(request):

     data = cartData(request)

     cartItems_quantity = data["cartItems"]
     order = data["order"]
     items = data["items"]

     context = {
          "items": items,
          "order": order,
          "cartItems_quantity": cartItems_quantity
     }
     return render(request, 'store/checkout.html', context)

def updateItem(request):
     data = json.loads(request.body)
     product_id = data["id"]
     action = data["action"]

     customer = request.user.customer
     product = Product.objects.get(id=product_id)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)
     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

     if action == "add":
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == "remove":
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if(orderItem.quantity <= 0):
          orderItem.delete()

     return JsonResponse("Item was added", safe=False)

def processOrder(request):

     print(f"Data: {request.body}")
     transaction_id = datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
     else:
          order, customer = guestOrder(request, data)

     total = float(data["userInfo"]["total"])
     order.transaction_id = transaction_id

     if total == float(order.get_total):
          order.complete = True
     order.save()

     if order.shipping:
          ShippingAddress.objects.create(
               customer=customer,
               order=order,
               address=data["shippingInfo"]["address"],
               city=data["shippingInfo"]["city"],
               state=data["shippingInfo"]["state"],
               zipcode=data["shippingInfo"]["zipcode"]
          )

     return JsonResponse("Payment completed", safe=False)