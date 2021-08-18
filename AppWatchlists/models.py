from django.db import models
from AppDips.models import StockNames
from Accounts.models import Account
# Create your models here.

class Watchlist(models.Model):
    watchlist_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.watchlist_id


class WatchlistItem(models.Model):
    company = models.ForeignKey(StockNames, on_delete=models.CASCADE)
    watchlist = models.ForeignKey(Watchlist,on_delete=models.CASCADE)
    high52 = models.FloatField(default=0.0)
    low52 = models.FloatField(default=0.0)
    lastPrice = models.FloatField(default=0.0)
    price_list = models.CharField(max_length=250,blank=True)

    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)

# class PriceList(models.Model):
#     watchlist_price_list = models.ForeignKey(WatchlistItem, on_delete=models.CASCADE)
    
    
#     def __str__(self):
#         return str(self.watchlist_price_list)
