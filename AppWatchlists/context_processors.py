from .models import Watchlist,WatchlistItem
from .views import _watchlist_id

def counter(request):
    watchlist_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            watchlist = Watchlist.objects.filter(watchlist_id=_watchlist_id(request))
            if request.user.is_authenticated:
                watchlist_items = WatchlistItem.objects.all().filter(user=request.user)
                print("watchlist_items1--------cpA",watchlist_items)
            else:
                watchlist_items = WatchlistItem.objects.all().filter(watchlist=watchlist[:1])
                print("watchlist_items2--------cpNa",watchlist_items)
            for watchlist_item in watchlist_items:
                watchlist_count +=1
        except Watchlist.DoesNotExist:
            watchlist_count = 0
    return dict(watchlist_count=watchlist_count)