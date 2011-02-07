from django.utils.translation import ugettext_lazy as _

# General constants
DELIMITER = '-'
CUSTOM_VALUE = 'custom'

# Simple level settings
LEVEL_VERYLOW = 1
LEVEL_LOW = 2
LEVEL_MEDIUM = 3
LEVEL_HIGH = 4
LEVEL_VERYHIGH = 5

LEVEL_CHOICES_QUICKACCESS = {
    LEVEL_VERYLOW: (_('Very low'), 'level_verylow'),
    LEVEL_LOW: (_('Low'), 'level_low'),
    LEVEL_MEDIUM: (_('Medium'), 'level_medium'),
    LEVEL_HIGH: (_('High'), 'level_high'),
    LEVEL_VERYHIGH: (_('Very high'), 'level_veryhigh')
}

LEVEL_CHOICES_MODEL = (
    (LEVEL_VERYLOW, _('Very low')),
    (LEVEL_LOW, _('Low')),
    (LEVEL_MEDIUM, _('Medium')),
    (LEVEL_HIGH, _('High')),
    (LEVEL_VERYHIGH, _('Very high'))
)

LEVEL_CHOICES_FORM = LEVEL_CHOICES_MODEL

# Duration range settings
DURATION_QUICK = ('0', '10')
DURATION_MEDIUM = ('10', '30')
DURATION_LONG = ('30', '60')
DURATION_VERYLONG = ('60', '720')

DURATION_CHOICES = (
    (DELIMITER.join(DURATION_QUICK), _('Quick (0-10 min)')),
    (DELIMITER.join(DURATION_MEDIUM), _('Medium (10-30 min)')),
    (DELIMITER.join(DURATION_LONG), _('Long (30-60 min)')),
    (DELIMITER.join(DURATION_VERYLONG), _('Very long (60+ min)')),
    (CUSTOM_VALUE, _('Custom range'))
)

# Price range settings
PRICE_VERYLOW = ('0', '2')
PRICE_LOW = ('2', '5')
PRICE_MEDIUM = ('5', '10')
PRICE_HIGH = ('10', '20')
PRICE_VERYHIGH = ('20', '120')

PRICE_CHOICES = (
    (DELIMITER.join(PRICE_VERYLOW), _('Very low (0-2 EUR)')),
    (DELIMITER.join(PRICE_LOW), _('Low (2-5 EUR)')),
    (DELIMITER.join(PRICE_MEDIUM), _('Medium (5-10 EUR)')),
    (DELIMITER.join(PRICE_HIGH), _('High (10-20 EUR)')),
    (DELIMITER.join(PRICE_VERYHIGH), _('Very high (20+ EUR)')),
    (CUSTOM_VALUE, _('Custom range'))
)

# Vegetarian/Vegan settings
VEG_YES = 1
VEG_NO = 0
VEG_BOTH = 2

VEG_CHOICES = (
    (VEG_YES, _('Yes')),
    (VEG_NO, _('No')),
    (VEG_BOTH, _('Doesn\'t matter'))
)