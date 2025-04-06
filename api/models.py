from django.db import models

# Create your models here.

class WishList(models.Model):
  name = models.TextField(max_length=240)
  tickers = models.JSONField(default=list)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.name}'

