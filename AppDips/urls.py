from django.urls import path
from AppDips import views


urlpatterns = [
    path('',views.home,name='home'),
    path('search/',views.search,name='search'),
    path('autosuggest/',views.autosuggest,name='autosuggest'),

]
