from django.db import models
from django.conf import settings
from django.db.models import Sum

class Company(models.Model):
    summary_amount = models.PositiveIntegerField()
    rate = models.FloatField()

    def get_amount(self, start_date, end_date):
        leased_amount = self.lease_set.filter(
            end_date__gte=start_date,
            start_date__lte=end_date).aggregate(
                Sum('amount')).get('amount__sum')
        amount = self.summary_amount
        if leased_amount:
            amount -= leased_amount
        return amount


class Lease(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.PositiveIntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    company = models.ForeignKey(Company)
