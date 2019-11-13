from django.db import models
from datetime import date

class Analyzer(models.Model):

    Date            = models.DateField()
    Open            = models.DecimalField(max_digits=10, decimal_places=2)
    Close           = models.DecimalField(max_digits=10, decimal_places=2)
    High            = models.DecimalField(max_digits=10, decimal_places=2)
    Low             = models.DecimalField(max_digits=10, decimal_places=2)
    Shares_Traded   = models.IntegerField(null=False, blank=True)
    Turnover        = models.DecimalField(max_digits=10, decimal_places=2)
    created_at      = models.DateField(auto_now_add=True)
    created_by      = models.CharField(max_length=100)
    updated_at      = models.DateField(auto_now_add=True)
    updated_by      = models.CharField(max_length=100,blank=True, default='') # Optional on create
    status          = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']

    # string representation of all the fields
    def __str__(self):
        return "{0} ".format(self.status)
