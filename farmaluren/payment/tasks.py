from io import BytesIO
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from orders.models import Order
from django.conf import settings

@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)

    subject = f"farmaluren - Invoice no. INV{order.id}"
    message = "Please, find attached the invoice for your recent purchase."
    email = EmailMessage(
        subject = subject,
        body = message,
        from_email = settings.EMAIL_HOST_USER,
        to = [order.email]
        )

    html = render_to_string('orders/order/pdf.html', {'order':order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    email.attach(f'oroder_{order.id}.pdf', out.getvalue(), 'application/pdf')
    email.send()