from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id, first_name):
    """Task to send an email"""
    order = Order.objects.get(id=order_id)
    subject = f"Order number: {order.id}"
    message = f"Dear { first_name},\n\n"\
        f"You have successfully placed an order."\
            f"Your order ID is {order.id}."
    mail_sent = send_mail(subject, message,"eogyateng@st.ug.edu.gh",[order.user])
    return mail_sent

@shared_task
def payment_completed(order_id,first_name):
    """Task to send an email when the payment was successful"""
    order = Order.objects.get(id = order_id)
    subject = f'Order with ID {order.id} Payment'
    message = f'Dear{first_name},\n\n Your payment for Order {order.id} was successful'
    mail_sent = send_mail(subject,message,"eogyateng@st.ug.edu.gh",[order.user])
    return mail_sent

@shared_task
def payment_not_completed(order_id,first_name):
    """Task to send an email when the payment was not successful"""
    order = Order.objects.get(id = order_id)
    subject = f'Order with ID {order.id} Payment'
    message = f'Dear{first_name},\n\n Your payment for Order {order.id} was not successful, please re-place order and make payment again'
    mail_sent = send_mail(subject,message,"eogyateng@st.ug.edu.gh",[order.user])
    return mail_sent
