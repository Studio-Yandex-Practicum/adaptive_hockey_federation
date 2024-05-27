from typing import Any, Dict, List

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def render_email_message(
    subject: str,
    context: Dict[str, Any],
    from_email: str,
    to: List[str],
    template: str,
) -> EmailMultiAlternatives:
    """Функция визуализации электронного письма из html-шаблона."""
    html_body = render_to_string(template, context)
    email = EmailMultiAlternatives(
        subject=subject,
        from_email=from_email,
        to=to,
    )
    email.attach_alternative(html_body, "text/html")
    return email
