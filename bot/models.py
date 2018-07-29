from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
# from bot.forms import *
# Create your models here.

trading_mode_choices = (('paper_trading', 'Paper Trading'),
                        ('live_trading', 'Live Trading'))

gender_choices = (('male', 'Male'),
                  ('female', 'Female'),
                  ('other', 'Other'))


class Contact(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(max_length=1500, default='', blank=True, null=True)

    def __str__(self):
        return self.name


class EmailSubscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField()
    name = models.CharField(max_length=100, default='')
    email = models.EmailField()
    phone = models.IntegerField(null=False)
    phone2 = models.IntegerField(null=True, blank=True)
    dob = models.DateField(auto_now=False, blank=True, null=True)
    gender = models.CharField(choices=gender_choices, null=False, max_length=10, default='male')
    address = models.TextField(max_length=500, blank=True)
    occupation = models.CharField(max_length=100, null=True)
    overview = models.TextField(max_length=1000, null=True)
    update_at = models.CharField(max_length=255, default='', blank=True, null=True)

    # class Meta:
    #     managed = False
    #     db_table = 'user_profile'


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email = models.EmailField(default=False)
#     # phone = models.IntegerField(null=True, blank=True)
#
#     def __str__(self):
#         return self.user.username
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Exchange(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30)
    key = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    other = models.CharField(max_length=300, default='', blank=True, null=True)


class Setting(models.Model):
    user = models.OneToOneField(User)
    trading_mode = models.CharField(choices=trading_mode_choices, max_length=20)
    coin_used = models.CharField(max_length=10)
    stop_loss_percent = models.CharField(max_length=10)
    max_profit = models.CharField(max_length=10)
    updated_at = models.CharField(max_length=255, default='', blank=True, null=True)
