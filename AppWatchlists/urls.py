from django.urls import path
from . import views

urlpatterns = [
    path('',views.watchlist,name='watchlist'),
    path('add_watchlist/<int:stocknames_id>/',views.add_watchlist,name='add_watchlist'),
    path('remove_btn/<int:stocknames_id>/<int:watchlist_item_id>/',views.remove_btn,name='remove_btn'),

]