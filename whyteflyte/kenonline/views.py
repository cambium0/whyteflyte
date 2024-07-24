from django.shortcuts import render, redirect
from .models import *
from kenonline.forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pathlib as pl
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

"""
def download(request):
    data = json.loads(request.body)
    file_path = 'static/kenonline/audio/' +  data['file_name']
    with ZipFile(file_path, 'w') as myzip:
        myzip.write('ken_tunes.zip')
    f_name = ken_tunes.zip
    print(f"file_path is {file_path}")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response["ContentDisposition"] = 'attachment; filename=' + f_name
            return response
    raise Http404
"""

def process_order(request):

    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)


    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        if order.shipping == True:
            ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
    else:
        customer, order = guestOrder(request, data)

    print("form data in /process_order is " + str(data))
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True

    order.save()
    d_files = []

    for item in order.orderitem_set.all().iterator():
        d_files.append(item.product.name)
    print("purchased files are " + str(d_files))
    request.session['do_download'] = d_files
    print("request.session['do_download'] is " + str(request.session['do_download']))
    # end comment

    if order.shipping == True:
        ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
        )
    ret_string = JsonResponse('Payment submitted..', safe=False)
    print("returning " + str(ret_string))

    return JsonResponse('Payment submitted..', safe=False)


def update_item(request):
    user = request.user
    data = json.loads(request.body)
    action = data['action']
    productId = data['productId']
    print('Action:', action)
    print('Product:', productId)

    print("user is " + str(user))
    
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

    return JsonResponse("item was added", safe=False)


def get_item(dictionary, key):
    varmint = "bugsbunny"
    return dictionary.get(key)


def home(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']


    products = Product.objects.all()
    context = {'products':products, 'items': items, 'order':order, 'cartItems':cartItems}
    return render(request, "kenonline/index.html", context)


def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            customer = Customer(user=user, name=user.username, email=user.email)
            customer.save()

            return redirect("my_login")

    context = {'registerform': form}

    return render(request, "kenonline/register.html", context=context)


def my_login(request):

    form = LoginForm()

    global user

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

    if form.is_valid():

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)

            return redirect("home")
        else:
            print("user is None apparently--authentication failed.")
    context = {'loginform':form}
    return render(request, "kenonline/my_login.html", context=context)


def my_logout(request):
    auth.logout(request)
    return redirect("home")


def store(request):


    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    # print("cartItems: " + str(cartItems) + "\norder: " + str(order) + "\nitems: " + str(items) + "\n")

    soundfiles = []
    #my_products = Product.objects.all()
    my_products = Product.objects.all()[:7]
    for product in my_products:
        if 'mp3' in product.name:
            soundfiles.append(product)

    # if request.user.is_authenticated:
    try:
        d_files = request.session['do_download']
        # print("request.session['do_download'] is " + str(request.session['do_download']))
        # print("sending d_file as 'do_download' in context to store.html; d_file is " + str(d_files))
        request.session['do_download'] = None
        context = {'products':soundfiles, 'cartItems': cartItems, 'do_download': d_files}
    except KeyError:
         # print("In except, request.session['do_download'] raised exception")
         context = {'products':soundfiles, 'cartItems': cartItems}
    return render(request,"kenonline/store.html", context=context)




def my_cart(request):

    # try:
        # if request.session['do_download']:
            # pass
    # except: 
        # request.session['do_download'] = "skip"

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "kenonline/my_cart.html", context)


def checkout(request):


    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "kenonline/checkout.html", context)


def user_logout(request):

    auth.logout(request)

    return redirect("home")

def cancel_order(request):

    transaction_id = request.query_params
    print("query_params are " + query_params)

    return redirect("store")