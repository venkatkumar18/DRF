from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_mail_on_order_creation(order_id, email):
    subject = "Order has been received"
    content = f"Your Order - {order_id} Has Been Accepted, Further Details Will Be Updated"
    print("INSIDE SEND MAIL CELERY FUNCTION")
    print(subject)
    print(content)
    return send_mail(subject=subject, message=content, 
                     from_email=settings.DEFAULT_FROM_EMAIL,recipient_list=[email],fail_silently=True)
