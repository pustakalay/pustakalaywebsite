from django.db import models

from billing.models import BillingProfile
from django.core.urlresolvers import reverse

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile)
    address_name    = models.CharField(max_length=120, null=True, blank=True, help_text='Name this address.')
    name            = models.CharField(max_length=120, null=True, blank=True, help_text='Shipping to?')
    phone           = models.CharField(max_length=10)
    address_line_1  = models.CharField(max_length=120)
    address_line_2  = models.CharField(max_length=120, null=True, blank=True)
    city            = models.CharField(max_length=120)
    country         = models.CharField(max_length=120, default='India')
    state           = models.CharField(max_length=120)
    postal_code     = models.CharField(max_length=120)

    def __str__(self):
        if self.address_name:
            return str(self.address_name)
        return str(self.address_line_1)
    
    def get_absolute_url(self):
        return reverse("addresses:address-update", kwargs={"pk": self.pk})
    
    def get_short_address(self):
        for_name = self.name 
        if self.address_name:
            for_name = "{} | {},".format( self.address_name, for_name)
        return "{for_name} {phone_number} {line1}, {city}".format(
                for_name = for_name or "",
                phone_number = self.phone,
                line1 = self.address_line_1,
                city = self.city
            ) 
    
    def get_address(self):
        return "{for_name}\n{phone_number}\n{line1}\n{line2}\n{city}\n{state}, {postal}\n{country}".format(
                for_name = self.name or "",
                phone_number = self.phone,
                line1 = self.address_line_1,
                line2 = self.address_line_2 or "",
                city = self.city,
                state = self.state,
                postal= self.postal_code,
                country = self.country
            )
