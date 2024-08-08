#!/usr/bin/env python
# encoding: utf-8

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def update_staff(sender, instance, created, **kwargs):
    if created:
        print(f"create new instance: {instance}")
        instance.is_staff = True
        instance.save()