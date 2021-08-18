from django.db import models

# Create your models here.

class StockNames(models.Model):
    symbol = models.CharField(max_length = 264,unique=True)
    companyName = models.CharField(max_length = 264)
    # slug = models.SlugField(max_length=50,unique=True)

    class Meta:
        verbose_name = 'StockNames'
        verbose_name_plural = 'StockNames'

    def __str__(self):
        return self.symbol
