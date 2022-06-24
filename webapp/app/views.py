from django.shortcuts import render, redirect
from django.contrib import messages

import requests

from app import forms
from app.tools import user, account_url, product_url, order_url, save_user, load_user

# Create your views here.


def check_admin():
    global user
    if user.get("token", None) and user.get("username", None):
        headers = {"Authorization": f"Token {user.get('token', None)}"}
        response = requests.get(account_url + "is_admin/", headers=headers)
        if response.status_code == requests.codes.ok:
            user["is_admin"] = response.json()["is_admin"]
            save_user(user)
            user = load_user()


def get_info():
    global user
    if user.get("token", None) and user.get("username", None) and user.get("id", None):
        headers = {"Authorization": f"Token {user.get('token', None)}"}
        response = requests.get(account_url + f"{user.get('id')}/", headers=headers)
        if response.status_code == requests.codes.ok:
            response = response.json()
            user["is_auth"] = True
            user["first_name"] = response.get("first_name", None)
            user["last_name"] = response.get("last_name", None)
            user["phone"] = response.get("phone", None)
            user["email"] = response.get("email", None)
            save_user(user)
            user = load_user()
        else:
            user["is_auth"] = False


def index(request):
    return redirect("/home")


def home(request):
    global user

    ()
    check_admin()
    context = {}
    products = []
    next = None
    previous = None

    response = requests.get(product_url)
    if response.status_code == requests.codes.ok:
        products = response.json()

        if "next" in products and products["next"]:
            if "page=" in products["next"]:
                next = products["next"].split("page=")[1]
            else:
                next = 0
        if "previous" in products and products["previous"]:
            if "page=" in products["previous"]:
                previous = products["previous"].split("page=")[1]
            else:
                previous = 0

    # print(products)

    context.update(
        {"a_user": user, "products": products, "next": next, "previous": previous}
    )
    return render(request, template_name="index.html", context=context)


def next_page(request, page=None):
    global user
    get_info()
    check_admin()
    context = {}
    products = []
    next = None
    previous = None

    params = {"page": page} if page and page != 0 else None

    response = requests.get(product_url, params=params)
    if response.status_code == requests.codes.ok:
        products = response.json()

        if "next" in products and products["next"]:
            if "page=" in products["next"]:
                next = products["next"].split("page=")[1]
            else:
                next = 0
        if "previous" in products and products["previous"]:
            if "page=" in products["previous"]:
                previous = products["previous"].split("page=")[1]
            else:
                previous = 0
    # print(products)
    context.update(
        {"a_user": user, "products": products, "next": next, "previous": previous}
    )
    return render(request, template_name="index.html", context=context)


def login(request):
    form = forms.ConnectionForm(data=request.POST or None)

    if request.POST:
        if form.is_valid():
            # response = requests.post(login_url, json=form.cleaned_data)
            return redirect("/home")
    return render(request, template_name="login.html", context={"form": form})


def profile(request):
    global user
    headers = {"Authorization": f"Token {user.get('token', None)}"}
    response = requests.get(account_url + f"{user['id']}/", headers=headers)
    a_user = {}
    if response.ok:
        a_user = response.json()
    return render(
        request,
        template_name="profile.html",
        context={"a_user": user, "user_info": a_user},
    )


def view_product(request, pk):
    global user
    product = {}
    response = requests.get(product_url + f"{pk}/")
    if response.ok:
        product = response.json()
    return render(
        request,
        template_name="product.html",
        context={"a_user": user, "product": product},
    )


def add_product(request):
    global user
    form = forms.AddProductForm(data=request.POST or None)

    if request.POST:
        if form.is_valid():
            response = requests.post(product_url, json=form.cleaned_data)
            if not response.ok:
                response = response.json()
                if "non_field_errors" in response:
                    messages.error(request, response["non_field_errors"])
                if "details" in response:
                    messages.error(request, response["details"])
                messages.error(request, "Impossible d'ajouter un nouveau produit.")

            return redirect("/home")
    return render(
        request,
        template_name="add_product.html",
        context={"form": form, "a_user": user},
    )


def logout(request):
    global user
    user = {
        "is_auth": False,
        "is_admin": False,
    }
    save_user(user)
    user = load_user()
    return redirect("/home")


def signup(request):
    global user
    form = forms.CreateUserForm(data=request.POST or None)

    if request.POST:
        if form.is_valid():
            cleaned_data = form.cleaned_data.copy()
            cleaned_data.pop("password2")
            response = requests.post(account_url, json=form.cleaned_data)
            if response.ok:
                user["is_auth"] = False
                user["username"] = cleaned_data["username"]
                messages.info(request, "Votre inscription a été effectué avec succès")
            else:
                messages.info(
                    request,
                    "Votre inscription a échoué. Veuillez recommencer ou contact un administrateur.",
                )
                user["is_auth"] = False
            save_user(user)
            user = load_user()
            return redirect("/home")
    return render(request, template_name="register.html", context={"form": form})


def orders(request):
    global user
    orders = None
    response = requests.get(order_url + "user_orders/", params={"user": user["id"]})
    if response.ok:
        orders = response.json()
    # print(orders)
    return render(
        request,
        template_name="orders.html",
        context={"orders": orders, "a_user": user},
    )


def make_order(request, pk):
    global user
    data = {"client": user["id"], "quantity": 1, "product": pk}
    response = requests.post(order_url, json=data)
    if not response.ok:
        response = response.json()
        if "non_field_errors" in response:
            messages.error(request, response["non_field_errors"])
        if "details" in response:
            messages.error(request, response["details"])
        messages.error(request, "Impossible d'effectuer une commande.")

    return redirect("/home")
