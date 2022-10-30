"""Views.py file for shop"""
import time
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.response import Response
from cart.forms import CartAddProductForm
from shop.api.serializer import CategorySerializer, ProductSerializer

from shop.forms import ProductCreateForm, SearchForm, ContactUs
from shop.models import Category, Product


# Create your views here.
def product_list(request, category_slug=None):
    """Products list view"""
    form = SearchForm()
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts= paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
        paginator = Paginator(products, 9)
        try:
            posts = paginator.page(1)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
    return render(request, "shop/index.html", {"category": category,"prod":products,
                                                      "categories": categories,
                                                      "post":posts,"page":page,"form_search":form})

def product_detail(request, id, slug):
    """Product detial"""
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    form = SearchForm()
    return render(request, "shop/details.html", {"product": product,"categories":categories,
    "cart_product_form":cart_product_form,"form_search":form})



class ProductPostSerializer(generics.ListAPIView):
    """Book list API View"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def post(self, request, *args, **kwargs):
        """Post method for HTTP POST request from Booklist View"""
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "details": "book added successfully",
                "data": {
                    "category": serializer.data["category"],
                    "name": serializer.data["name"],
                    "description": serializer.data["description"],
                    "price": serializer.data["price"],
                    "image": serializer.data["image"]
                }
            })
        return Response({
            "status": "failure",
            "details": serializer.errors})

class CategoryAddSerializer(generics.ListAPIView):
    """Catalogue list API View"""
    queryset = Category.objects
    serializer_class = CategorySerializer
    def post(self, request):
        """Post method for HTTP POST request from Catalogue View"""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "details": "catalogue created",
                "data": {
                    "name": serializer.data["name"]
                }}, status=status.HTTP_201_CREATED)
        return Response({
            "status": "failure",
            "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)

def add_product(request):
    """Adding products to the page"""
    forms = SearchForm()
    if request.method == "POST":
        form =ProductCreateForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully")
            return redirect(reverse('shop:shop'))
    form = ProductCreateForm()
    return render(request, "shop/add_product.html", {"form": form,"form_search":forms})


def post_search(request):
    """Creating the get post search function"""
    form = SearchForm()
    categories = Category.objects.all()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            lookups = (Q(name__icontains=query)|
                  Q(description__icontains=query)|
                  Q(category__name__icontains=query))
            results = Product.objects.filter(lookups).distinct()
    paginator = Paginator(results, 9)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts= paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "shop/search.html",{
        "form_search":form,"query":query, "results":results, "post":posts,"categories":categories
    })


def contact_us(request):
    """View for contact us page"""
    form = ContactUs()
    if request.method =="POST":
        forms = ContactUs(request.POST)
        if forms.is_valid():
            cleaned  = forms.cleaned_data
            # sending email from contact me page.
            send_mail(subject=cleaned["subject"], message =
            f'{cleaned["message"]}\n From: {cleaned["email"]} \n Telephone: {cleaned["phone"]}',
            from_email="eogyateng@st.ug.edu.gh",recipient_list=["gyateng94@gmail.com"])
            #Sending a back email to user after reecieving the email from contact me
            send_mail(subject="Email Recieved",
            message ='Your message was received and we will reach out to you shortly. \n\n Regards',
            from_email="eogyateng@st.ug.edu.gh",recipient_list=[cleaned["email"]])
    categories = Category.objects.all()
    return render(request,"shop/contact.html",{"contact":form, "categories":categories})
