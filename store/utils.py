import json
from .models import Customer,OrderItem,Product,Order,ShippingAddress

def cookieCart(request):

    try:
        cart = json.loads(request.COOKIES["cart"])
    except KeyError:
        cart = {}

    items = []
    order = {
        "get_total": 0,
        "get_quantity": 0,
        "shipping": False
    }

    cartItems_quantity = order["get_quantity"]

    for i in cart:
        try:
            cartItems_quantity += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order["get_total"] += total
            order["get_quantity"] += cart[i]["quantity"]

            item = {
                    "product": {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "imageURL": product.imageURL
                    },
                    "quantity": cart[i]["quantity"],
                    "get_total": total
            }
            items.append(item)

            if product.digital == False:
                    order["shipping"] = True
        except:
            pass
    return {
        "cartItems": cartItems_quantity, 
        "order": order, 
        "items": items
    }

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems_quantity = order.get_quantity
    else:
        cookieData = cookieCart(request)
        cartItems_quantity = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]

    return {
        "cartItems": cartItems_quantity, 
        "order": order, 
        "items": items
    }

def guestOrder(request, data):
    print("User is not logged in")

    print("COOKIES: ", request.COOKIES)
    name = data["userInfo"]["name"]
    email = data["userInfo"]["email"]

    cookieData = cookieCart(request)
    items = cookieData["items"]

    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item["product"]["id"])
        quantity = item["quantity"]
        orderItem = OrderItem.objects.create(
            product=product,
            order = order,
            quantity=quantity
        )

    return order, customer