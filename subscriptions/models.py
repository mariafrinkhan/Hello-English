from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from quiz.models import *
from django.conf import settings

class Plan(models.Model):
    DISCOUNT_CHOICES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    yearly_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    choice = models.CharField(
        max_length=10,
        choices=DISCOUNT_CHOICES,
        default='monthly'
    )
    
    discount = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=0.0,
        help_text="Discount percentage"
    )
    
    monthly_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    yearly_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    
    popular = models.BooleanField(default=False)
    # button_text = models.CharField(max_length=100, blank=True)
    # button_variant = models.CharField(max_length=50, blank=True)
    # color = models.CharField(max_length=20, blank=True)
    # icon = models.CharField(max_length=100, blank=True)
    month= models.PositiveIntegerField(default=0, null=True, blank=True)
    year= models.PositiveIntegerField(default=0, null=True, blank=True)

    quizzes = models.ManyToManyField('quiz.Quiz', related_name='plans', blank=True)

    def __str__(self):
        return self.title
    
    # def discounted_price(self, period='month'):
    #     """Return price after applying admin-set discount."""
    #     if period == 'month' and self.month > 0:
    #         return self.monthly_price * (1 - self.monthly_discount / 100)
    #     elif period == 'year' and self.year > 0:
    #         return self.yearly_price * (1 - self.yearly_discount / 100)
    #     return 0


class Feature(models.Model):
    plan = models.ForeignKey(Plan, related_name='features', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, related_name='user_subscriptions')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    mobile = models.CharField(max_length=15, blank=True, null=True)
    


    def save(self, *args, **kwargs):
        if self.plan and not self.end_date:
            days = self.plan.month * 30 + self.plan.year * 365
            self.end_date = self.start_date + timezone.timedelta(days=days)
        super().save(*args, **kwargs)
        
    # def discounted_price(self, period='month'):
    #     """Return the subscription price after applying plan's admin-set discount."""
    #     if not self.plan:
    #         return 0
    #     return self.plan.discounted_price(period)

    def __str__(self):
        plan_name = self.plan.title if self.plan else "No Plan"
        return f"{self.user.username} - {plan_name}"

    
