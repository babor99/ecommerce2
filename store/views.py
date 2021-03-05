from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime

from .models import *
from .forms import ContactForm
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def store(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    products = Product.objects.all()

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)



def cart(request):
    data = cartData(request)
    
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)



def checkout(request):
    data = cartData(request)

    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('product id:', productId)
    print('Action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1) 
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)



def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print('Data', data)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )     
    return JsonResponse('Payment complete', safe=False)



def search(request):
    data = cartData(request)
    cartItems = data['cartItems']

    search_keyword = request.GET['search_keyword']
    searched_products = Product.objects.filter(name__icontains=search_keyword)
    context = {'searched_products': searched_products, 'cartItems': cartItems}
 
    return render(request, 'store/search.html', context)



def about(request):
    data = cartData(request)
    cartItems = data['cartItems']
    context = {'cartItems': cartItems}

    return render(request, 'about.html', context)



def contact(request):
    data = cartData(request)
    cartItems = data['cartItems']

    form = ContactForm
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form = ContactForm
    context = {'cartItems': cartItems, 'form':form}

    return render(request, 'contact.html', context)