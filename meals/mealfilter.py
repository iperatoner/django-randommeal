from .models import Meal

# TODO:
# I probably won't need the exclude methods,
# because everything can be done through filters
# (checkboxes in interface)

class MealFilter(object):
    def __init__(self, queryset=None):
        self.queryset = queryset
        self.exclude_args = {}
        self.filter_args = {}
        
    def general_action(self, action, model_field, value):
        """
        Executes a general action, like filtering or excluding
        specific stuff (`value`) on a specific field
        (`model_field`, also including django's magic `__in` and `__range` stuff)
        """
        assert action in ['filter', 'exclude']
        if action == 'filter':
            self.filter_args[model_field] = value
        elif action == 'exclude':
            self.exclude_args[model_field] = value


    def filter_complexity(self, complexity_levels):
        """Filters a specific rate of complexity out of the queryset."""
        self.general_action('filter', 'complexity__in', complexity_levels)

    def filter_nutrient_content(self, nc_levels):
        """Filters a specific rate of nutrient content out of the queryset."""
        self.general_action('filter', 'nutrient_content__in', nc_levels)


    def filter_duration(self, range, range_from=False, range_to=False):
        """Filters a specific range of duration out of the queryset."""
        if range_from and range_to:
            range = (range_from, range_to)
        self.general_action('filter', 'duration__range', range)

    def filter_price(self, range, range_from=False, range_to=False):
        """Filters a specific range of price out of the queryset."""
        if range_from and range_to:
            range = (range_from, range_to)
        self.general_action('filter', 'price__range', range)
        
        
    def filter_vegetarian(self, vegetarian):
        """Includes or excludes vegetarian meals into or from the queryset."""
        self.general_action('filter', 'vegetarian', vegetarian)
        
    def filter_vegan(self, vegan):
        """Includes or excludes vegan meals into or from the queryset."""
        self.general_action('filter', 'vegan', vegan)


    def bind(self, qs):
        """Bind a Queryset of Meals to the MealFilter."""
        self.queryset = qs
        
    def execute(self):
        """Applies all saved actions onto the queryset."""
        if self.queryset is not None:
            return self.queryset.filter(**self.filter_args)
        else:
            return Meal.objects.filter(**self.filter_args)