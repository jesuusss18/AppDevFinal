from django.db import models
from django.utils import timezone

class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.FloatField(default=0)
    income = models.FloatField(default=0)
    expense = models.FloatField(default=0)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    saving_goal = models.FloatField(default=0)
    liability_list = models.ManyToManyField('Liability', blank=True)
    salary = models.FloatField(default=0)

class Liability(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField(default=0)
    date = models.DateField(default=timezone.now)
    long_term = models.BooleanField(default=False)
    interest_rate = models.FloatField(default=0, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    monthly_expense = models.FloatField(default=0, blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Calculate monthly expense for long-term liabilities
        if self.long_term:
            self.monthly_expense = self.calculate_monthly_expense()
        super(Liability, self).save(*args, **kwargs)

    def calculate_monthly_expense(self):
        if self.long_term:
            if not self.end_date:
                raise ValueError("End date must be provided.")
            if self.interest_rate == 0:
                return self.amount / ((self.end_date - self.date).days / 30)
            months = (self.end_date.year - self.date.year) * 12 + self.end_date.month - self.date.month
            if months <= 0:
                raise ValueError("End date must be later than start date.")
            monthly_rate = self.interest_rate / 12 / 100
            return round((self.amount * monthly_rate) / (1 - (1 + monthly_rate) ** -months), 2)
        return self.monthly_expense
