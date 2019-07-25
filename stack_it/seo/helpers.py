from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.redirects.models import Redirect
from django.conf import settings


def handle_redirection(full_paths):
    """
    Create-or Update redirections to instance for each paths given in full_paths

    Args:
        full_paths (list): List of str, giving which paths need redirection
    """
    for old_full_path, new_full_path in full_paths:
        if old_full_path == new_full_path:
            continue
        try:
            with transaction.atomic():
                Redirect.objects.create(
                    old_path=old_full_path,
                    new_path=new_full_path,
                    site_id=settings.SITE_ID,
                )
        except IntegrityError:
            Redirect.objects.filter(
                old_path=old_full_path, site_id=settings.SITE_ID
            ).update(new_path=new_full_path)
        Redirect.objects.filter(
            new_path=old_full_path, site_id=settings.SITE_ID
        ).update(new_path=new_full_path)

