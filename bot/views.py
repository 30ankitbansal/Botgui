import json

from django.contrib.auth import login, authenticate, logout
# import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
# from user.models import Profile

from bot.forms import *
from binance_feed.models import *
from binance_feed.api.binance import *


def index(request):
    return render(request, "index.html")


def dashboard(request):
    if request.user.is_authenticated():
        # print('1111')
        currency_pairs = History.objects.order_by('symbol').values_list('symbol', flat=True).distinct()
        # print(currency_pairs)
        # print(len(currency_pairs))

        return render(request, "dashboard.html", {'currency_pairs': currency_pairs})
    else:
        return HttpResponseRedirect('/index/')


def index3(request):
    return render(request, "index-3.html")


def services(request):
    return render(request, 'services.html')


def about(request):
    return render(request, 'about.html')


def error(request):
    return render(request, "404.html")


def blog_details(request):
    return render(request, 'blog-details.html')


def blog_list(request):
    return render(request, 'blog-list.html')


def cart(request):
    return render(request, 'cart.html')


def comming_soon(request):
    return render(request, 'comming-soon.html')


# def login_signup(request):
#     return render(request, 'login-signup.html')


def product_details(request):
    return render(request, 'product-details.html')


def product_grid(request):
    return render(request, 'product-grid.html')


def product_list(request):
    return render(request, 'product-list.html')


def support(request):
    return render(request, 'support.html')


def logout_view(request):
    logout(request)
    return login_signup(request)


def login_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # profile_form = ProfileInlineFormset(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                user.email = form.cleaned_data.get('email')
                user.save()
                login(request, user)
                # print(user)
                return redirect('dashboard')
        else:
            # print(form.errors)
            msg = 'Please check your details!'

            if 'username' in form.errors:
                msg = 'username already exist'

            if 'password2' in form.errors:
                msg = 'Password didn\'t match'

            return render(request, 'login-signup.html', {'registerErrorMsg': msg, 'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'login-signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login-signup.html', {'loginErrorMsg': 'username password not match', 'form': form})
    else:
        form = LoginForm()

    return render(request, 'login-signup.html', {'form': form})


@csrf_exempt
def email_subscribe(request):
    if request.method == "POST":
        form = EmailSubscribeForm(request.POST)
        if form.is_valid():
            print('valid')
            form.save()
            return HttpResponseRedirect('/index/')
        # except Exception as e:
        # print(e)
        # else:
    # # print('')
    return render(request, 'index.html', {'form': form})


@csrf_exempt
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # print('valid')
            form.save()
            return HttpResponseRedirect('/index/')
        # except Exception as e:
        # print(e)
        # else:
        # # print('')
        return HttpResponseRedirect('/contact/')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            setting, created = Setting.objects.get_or_create(user=request.user)
            print(setting)
            print(type(setting))
            setting.coin_used = form.cleaned_data.get('coin_used')
            setting.trading_mode = form.cleaned_data.get('trading_mode')
            setting.stop_loss_percent = form.cleaned_data.get('stop_loss_percent')
            setting.max_profit = form.cleaned_data.get('max_profit')
            setting.updated_at = datetime.datetime.now()
            setting.save()
            exchange, created = Exchange.objects.get_or_create(user=request.user)
            exchange.name = 'binance'
            exchange.key = form.cleaned_data.get('key')
            exchange.secret = form.cleaned_data.get('secret')
            exchange.save()
            return HttpResponseRedirect('/settings/')
        return HttpResponseRedirect('/settings/')
    elif request.user.is_authenticated():
        try:
            exchange = Exchange.objects.get(user=request.user)
            try:
                setting = Setting.objects.get(user=request.user)
                # print(setting.trading_mode)
                return render(request, "settings.html", {'key': exchange.key, 'secret': exchange.secret,
                                                         'trading_mode': setting.trading_mode,
                                                         'coin_used': setting.coin_used,
                                                         'stop_loss_percent': setting.stop_loss_percent,
                                                         'max_profit': setting.max_profit})
            except:
                pass
            return render(request, "settings.html", {'key': exchange.key, 'secret': exchange.secret})
        except:
            return render(request, "settings.html")
    else:
        return HttpResponseRedirect('/index/')


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/settings/')
        return HttpResponseRedirect('/settings/')
    elif request.user.is_authenticated():
        # If a user is logged in, redirect them to a page informing them of such
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            print(user_profile)
            # response = {'name': user_profile.name, 'email': user_profile.email,
            #             'phone': user_profile.phone, 'phone2': user_profile.phone2,
            #             'dob': user_profile.dob, 'gender': user_profile.gender,
            #             'address': user_profile.address, 'occupation': user_profile.occupation,
            #             'overview': user_profile.overview}
            # print(response)
            render(request, 'profile.html', {'name': user_profile.name, 'email': user_profile.email,
                                             'phone': user_profile.phone, 'phone2': user_profile.phone2,
                                             'dob': user_profile.dob, 'gender': user_profile.gender,
                                             'address': user_profile.address, 'occupation': user_profile.occupation,
                                             'overview': user_profile.overview, 'profile_picture': user_profile.avatar})
        except:
            # print(1111)
            render(request, "profile.html")
        return render(request, "profile.html")
    else:
        return HttpResponseRedirect('/index/')
