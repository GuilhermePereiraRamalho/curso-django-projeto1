from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import Recipe

import os


def delete_cover(instance):
    if not instance.cover:
        return

    cover_path = instance.cover.path
    if os.path.isfile(cover_path):
        try:
            os.remove(cover_path)
        except PermissionError:
            pass


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()
    delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.filter(pk=instance.pk).first()

    if not old_instance:
        return

    is_new_cover = old_instance.cover != instance.cover

    if is_new_cover:
        delete_cover(old_instance)
