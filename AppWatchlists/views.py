from django.shortcuts import render,redirect,get_object_or_404
from AppDips.models import StockNames
from .models import Watchlist,WatchlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from nsetools import Nse

#Email Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.

def _watchlist_id(request):
    watchlist = request.session.session_key
    if not watchlist:
        watchlist = request.session.create()
    return watchlist

@login_required(login_url= 'login')
def add_watchlist(request,stocknames_id):
    company = StockNames.objects.get(id=stocknames_id)
    in_wishlist = WatchlistItem.objects.filter(watchlist__watchlist_id=_watchlist_id(request)).exists()
    try:
        watchlist = Watchlist.objects.get(watchlist_id=_watchlist_id(request))
    except Watchlist.DoesNotExist:
        watchlist = Watchlist.objects.create(watchlist_id = _watchlist_id(request))
    
    watchlist.save()

    if request.user.is_authenticated:
        try:
            watchlist_item = WatchlistItem.objects.get(company=company,watchlist=watchlist,user=request.user)
            watchlist_item.save()
        except WatchlistItem.DoesNotExist:
            watchlist_item = WatchlistItem.objects.create(company=company,watchlist=watchlist,user=request.user)
            watchlist_item.save()
    else:
        try:
            watchlist_item = WatchlistItem.objects.get(company=company,watchlist=watchlist)
            watchlist_item.save()
        except WatchlistItem.DoesNotExist:
            watchlist_item = WatchlistItem.objects.create(company=company,watchlist=watchlist)
            watchlist_item.save()

    
    return redirect('watchlist')


def watchlist(request,watchlist_item=None):
    nse = Nse()
    try:
        if request.user.is_authenticated:
            # watchlist = Watchlist.objects.get(watchlist_id=_watchlist_id(request))
            watchlist_items = WatchlistItem.objects.filter(user=request.user,is_active=True)
            print("request.user----------",request.user)
            print("watchlist_items----------",watchlist_items[0])
        else:
            watchlist = Watchlist.objects.get(watchlist_id=_watchlist_id(request))
            watchlist_items = WatchlistItem.objects.filter(watchlist=watchlist)
        for watchlist_item in watchlist_items:
            symbol = watchlist_item.company.symbol
            quote = nse.get_quote(symbol)
            watchlist_item.high52 = quote['high52']
            watchlist_item.low52 = quote['low52']
            watchlist_item.lastPrice = quote['lastPrice']
            
            lst = []
            ans = quote['high52']
            res = (quote['high52'] - quote['low52'])/10
            for i in range(10):
                ans = ans-res
                lst.append(round(ans,2))
                ans = ans
            watchlist_item.price_list = lst
            watchlist_item.save()

            #Send Mail for price hit in price list
            if round(watchlist_item.lastPrice) in [round(num) for num in watchlist_item.price_list]:
                user=request.user
                current_site = get_current_site(request)
                mail_subject = "Price Dip Hit! for {}".format(watchlist_item.company)
                message = render_to_string("includes/price_dip_hit.html",{
                    'user' : user,
                    'domain' : watchlist_item.company.companyName,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token' : default_token_generator.make_token(user),
                })
                to_email = watchlist_items[0]
                send_email = EmailMessage(mail_subject , message, to=[to_email])
                send_email.send()

        context = {
            'watchlist_items':watchlist_items,
            }
    except ObjectDoesNotExist:
        return render(request,'watchlist.html')        
    
    return render(request,'watchlist.html',context)

def remove_btn(request,stocknames_id,watchlist_item_id):
    company = get_object_or_404(StockNames,id=stocknames_id)
    # print("remove===========",watchlist)
    if request.user.is_authenticated:
        watchlist_items = WatchlistItem.objects.get(company=stocknames_id,id= watchlist_item_id,user=request.user)
    else:
        watchlist = Watchlist.objects.get(watchlist_id=_watchlist_id(request))
        watchlist_items = WatchlistItem.objects.get(company=stocknames_id,watchlist= watchlist)
    watchlist_items.delete()
    return redirect('watchlist')


def send_mail():
    nse = Nse()
    try:
        if request.user.is_authenticated:
            watchlist_items = WatchlistItem.objects.filter(user=request.user,is_active=True)

            for watchlist_item in watchlist_items:
                #Send Mail for price hit in price list
                if round(watchlist_item.lastPrice) in [round(num) for num in watchlist_item.price_list]:
                    user=request.user
                    # current_site = get_current_site(request)
                    mail_subject = "Price Dip Hit! for {}".format(watchlist_item.company)
                    message = render_to_string("includes/price_dip_hit.html",{
                        'user' : user,
                        'domain' : watchlist_item.company.companyName,
                        'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                        'token' : default_token_generator.make_token(user),
                    })
                    to_email = watchlist_items[0]
                    send_email = EmailMessage(mail_subject , message, to=[to_email])
                    send_email.send()
    except ObjectDoesNotExist:
        pass




