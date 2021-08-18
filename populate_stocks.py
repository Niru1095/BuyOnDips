import os 
#to need to configure the settings for the project.
#actually need to run this before I call any code so I need to say OS environ for the environment.
os.environ.setdefault('DJANGO_SETTINGS_MODULE','BuyOnDips2.settings')
#And basically what this is doing is just configuring the settings for the project they need to do this before you start manipulating the actual models that are from here we can import Django and then setitup
import django
django.setup()
from nsetools import Nse
from AppDips.models import StockNames

def populate():
    print("HELLO Script")
    nse = Nse()
    all_stock_codes = nse.get_stock_codes()
    for i,j in all_stock_codes.items():
        sn = StockNames.objects.get_or_create(symbol=i,companyName=j)[0]
    #     sn.save()
    # return sn

if __name__ == '__main__':
    print("Populating Script")
    populate()
    print("Poplating Complete!")
