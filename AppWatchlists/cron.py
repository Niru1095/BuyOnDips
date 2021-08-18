from django.core.exceptions import ObjectDoesNotExist
from .models import Watchlist,WatchlistItem
# from .views import send_mail
from django.http import HttpRequest
#Email Verification
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from nsetools import Nse
import logging

logger = logging.getLogger(__name__)

def notifyuser():
    logger.info("CRon Job")
    # print("Mail Sent")
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



# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage


# @periodic_task(
# run_every=(crontab(hour=3, minute=34)), #runs exactly at 3:34am every day
# name="Dispatch_scheduled_mail",
# reject_on_worker_lost=True,
# ignore_result=True)
# def schedule_mail():
#     message = render_to_string('app/schedule_mail.html')
#     mail_subject = 'Scheduled Email'
#     to_email = getmail
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     email.send()