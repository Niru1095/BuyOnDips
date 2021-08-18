from django.shortcuts import render
from .models import StockNames
from AppWatchlists.models import WatchlistItem
from AppWatchlists.views import _watchlist_id
from django.db.models import Q
from django.http import JsonResponse
from nsetools import Nse

# Create your views here.

def home(request):
    return render(request,'home.html')

def search(request):
    nse = Nse()
    if 'search_keyword' in request.GET:
        search_keyword = request.GET['search_keyword']
        if search_keyword:
            company_key = StockNames.objects.filter(Q(companyName__startswith=search_keyword) | Q(symbol__icontains=search_keyword))
            in_watchlist = WatchlistItem.objects.filter(watchlist__watchlist_id=_watchlist_id(request))
            print("in_watchlist----------------",in_watchlist)
            symbol = str(company_key[0])
            quote = nse.get_quote(symbol)
            high52 = quote['high52']
            high_date = quote['cm_adj_high_dt']
            low52 = quote['low52']
            low_date = quote['cm_adj_low_dt']
            pChange = quote['pChange']
            lastPrice = quote['lastPrice']
            price_list = []
            res = (high52 - low52)/10
            ans = high52
            for i in range(10):
                ans = ans-res
                price_list.append(round(ans,2))
                ans = ans
            context = {
                'company_key': company_key, 
                'high52': high52, 
                'high_date': high_date, 
                'low52': low52, 
                'low_date': low_date,
                'price_list':price_list, 
                'pChange': pChange,
                'lastPrice': lastPrice,
                'in_watchlist' : in_watchlist,
                }
            return render(request,'stockpage.html',context)
        else:
            return render(request,'home.html')


def autosuggest(request):
    query_original = request.GET.get('term')
    query_set = StockNames.objects.filter(Q(companyName__contains=query_original)| Q(symbol__icontains=query_original))
    my_list = []
    my_list += [x.companyName for x in query_set]
    return JsonResponse(my_list,safe=False)
