from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from psycopg2 import OperationalError
from shop.models import Category
import weasyprint
from .models import Order
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.forms import SearchForm
from coupons.forms import CouponApplyForm
# Braintree
import braintree
from django.conf import settings
from orders.task import order_created, payment_completed,payment_not_completed
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

# from .tasks import order_created

# Create your views here.

@login_required
def order_create(request):
    """Creating the order"""
    forms = SearchForm()
    coupon_apply_form = CouponApplyForm()
    cart = Cart(request)
    if not request.session["cart"]:
        return redirect(reverse('cart:cart_detail'))
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.user = request.user
            first_name = request.user.first_name 
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item["product"], price=item["price"],
                                         quantity=item["quantity"])
            cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id, first_name)
            request.session['order_id'] = order.id
            return redirect(reverse('orders:process'))
    else:
        form = OrderCreateForm()
        return render(request, "orders/checkout.html", {"cart": cart,
        "form": form,"coupon_apply_form":coupon_apply_form,"form_search":forms})


@staff_member_required
def admin_order_detail(request, order_id):
    """Admin order details"""
    order = get_object_or_404(Order, id=order_id)
    return render(request, "admin/orders/order/admin_detail.html", {"order": order})

def order_detail(request, order_id):
    """User order details"""
    categories = Category.objects.all()
    order = get_object_or_404(Order, id=order_id)
    form = SearchForm()
    return render(request, "admin/orders/order/detail.html",
        {"order": order,"categories":categories,"form_search":form})


@staff_member_required
def admin_order_pdf(request, order_id):
    """Admin order view to PDF"""
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string("orders/pdf.html", {"order": order})
    response = HttpResponse(content_type='application/pdf')
    response["Content-Disposition"] = f"filename = order_{order_id}.pdf"
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(
        settings.STATIC_ROOT + "css/pdf.css")])
    return response
@login_required
def payment_process(request):
    """Payment view"""
    form = SearchForm()
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id= order_id)
    total_cost = order.get_total_cost()
    first_name = request.user.first_name
    if request.method =="POST":
        nonce = request.POST.get("payment_method_nonce", None)
        result = gateway.transaction.sale({
            "amount": f"{total_cost:.2f}",
            "payment_method_nonce":nonce,
            "options":{
                "submit_for_settlement":True
            }
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            # launch asynchronous task
            # payment_completed.delay(order.id,first_name)
            return redirect("orders:done")
        else:
            # payment_not_completed.delay(order.id,first_name)
            return redirect("orders:canceled")
    else:
        client_token = gateway.client_token.generate()
        return render(request,"orders/payment.html", {"client_token":client_token,
        "order":order, "form_search":form})
@login_required
def payment_done(request):
    """When payment goes through"""
    return render(request, "orders/done.html")
@login_required
def payment_canceled(request):
    """Canceled payments"""
    return render(request, "orders/canceled.html")


@login_required
def order_history(request):
    """Where user can  get order history"""
    order_list = Order.objects.filter(user_id =request.user.id)
    orders_id = Order.objects.filter(user_id =request.user.id).values_list("id", flat=True)
    orders = OrderItem.objects.filter(id__in = orders_id)
    categories = Category.objects.all()
    form = SearchForm()
    return render(request,"orders/order_history.html",
    {"orders":orders,"order_list":order_list,"categories":categories,"form_search":form})
