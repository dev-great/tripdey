import logging
from django.conf import settings
from django.dispatch import receiver
from authentication.models import UserBusiness
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string, TemplateDoesNotExist
from django_rest_passwordreset.signals import reset_password_token_created


logger = logging.getLogger(__name__)

User = get_user_model()


# PASSWORD RESET EMAIL
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    try:
        merge_data = {
            'titanium_training_user': reset_password_token.user.email,
            'otp': reset_password_token.key
        }

        try:
            html_body = render_to_string('otp_mail.html', merge_data)
        except TemplateDoesNotExist as template_error:
            logger.error(f"Template not found: {template_error}")
            html_body = f"Dear {reset_password_token.user.email},\n\nYour OTP is: {reset_password_token.key}\n\nPlease use this OTP to reset your password."

        msg = EmailMultiAlternatives(
            subject="Titanium Training Password Reset",
            from_email=settings.EMAIL_HOST_USER,
            to=[reset_password_token.user.email],
            body=" ",  # Leave this as is; it will be replaced by the alternative part
        )
        msg.attach_alternative(html_body, "text/html")

        try:
            msg.send(fail_silently=False)
        except BadHeaderError as header_error:
            logger.error(f"Invalid header found: {header_error}")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


@receiver(post_save, sender=UserBusiness)
def update_user_is_business(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.is_business = True
        user.save()
