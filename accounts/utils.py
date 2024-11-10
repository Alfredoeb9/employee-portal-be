import random
from django.conf import settings
from django.core.mail import EmailMessage
from .models import User, OneTimePassword

def generateOTP():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp

def send_otp_email(email):
    current_site = 'myAuth.com'
    otp_code = generateOTP()

    user = User.objects.get(email=email)

    email_subject = 'One Time Password for Email Verification'
    email_body = f'Hi, {user.first_name} thank you for signing up on {current_site} please verify your email with this One Time Password \n {otp_code}'
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, otp=otp_code)

    email = EmailMessage(
        from_email=from_email,
        subject=email_subject,
        body=email_body,
        to=[email],
    )
    email.send(fail_silently=True)

def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[data['to_email']]
    )

    email.send(fail_silently=True)