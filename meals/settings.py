from django.utils.translation import ugettext_lazy as _

# Level constants
VERYLOW = 1
LOW = 2
MEDIUM = 3
HIGH = 4
VERYHIGH = 5

# Tuple with possible level choices for a model field
LEVEL_CHOICES = (
    (VERYLOW, _('Very low')),
    (LOW, _('Low')),
    (MEDIUM, _('Medium')),
    (HIGH, _('High')),
    (VERYHIGH, _('Very high'))
)