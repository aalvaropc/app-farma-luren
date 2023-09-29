from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings

@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Orden nr. {order.id}'
    message = f'Estimado {order.first_name},\n\nHas realizado un pedido con éxito. Su ID de pedido es {order.id}.'
    mail_sent = send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.email]
    )
    return mail_sent