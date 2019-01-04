from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_neg_quantity(value):
    if value < 0:
        raise ValidationError(
            _('Quantity cannot be negative!!'),
            params={'value': value},
        )

def validate_max_quantity(value):
    if value > 10:
        raise ValidationError(
            _('Limited quantity is available!!'),
            params={'value': value},
        )

def validate_quantity(value):
    if value <= 0:
        raise ValidationError(
            _("Out of stock!!"),
            params={'value': value},
        )

def validate_add_quantity(value):
    if value < 1:
        raise ValidationError("Add the product with some quantity!!")

def validate_phoneno(value):
    if not((len(str(value)) == 10)):
        raise ValidationError(
            _("Phone no. must be of 10 digits!"),
            params={'value':value},
        )

def validate_address(value):
    if value is None:
        raise ValidationError("Enter the valid address!!")        
