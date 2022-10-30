"""Cart forms"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, Category
from shop.forms import SearchForm
from cart.cart import Cart
from cart.forms import CartAddProductForm
from coupons.forms import CouponApplyForm
# Create your views here.


@require_POST
def cart_add(request, product_id):
    """Adding cart item"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        cart.add(product=product, quantity=clean_data["quantity"],
                 override_quantity=clean_data["override"])
    return redirect("cart:cart_detail")


def cart_remove(request, product_id):
    """Removing item from cart"""
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return redirect("cart:cart_detail")
    except Product.DoesNotExist:
        return redirect("cart:cart_detail")



def cart_detail(request):
    """All items"""
    form = SearchForm()
    cart = Cart(request)
    categories = Category.objects.all()
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'], 'override': True})
    coupon_apply_form = CouponApplyForm()
    return render(request, "cart/details.html", {'cart': cart, "categories":categories,
    "coupon_apply_form": coupon_apply_form,"form_search":form})
