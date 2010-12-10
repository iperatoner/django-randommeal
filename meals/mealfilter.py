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
        
    def general_action(self, action, key, value):
        """
        Executes a general action, like filtering or excluding
        specific stuff (`value`) on a specific field
        (`key`, also including django's magic `__in` and `__range` stuff)
        """
        assert action in ['filter', 'exclude']
        if action == 'filter':
            try:
                self.filter_args[key] = self.filter_args[key].append(value)
            except KeyError:
                self.filter_args[key] = []
                self.filter_args[key] = self.filter_args[key].append(value)
        elif action == 'exclude':
            try:
                self.exclude_args[key] = self.exclude_args[key].append(value)
            except KeyError:
                self.exclude_args[key] = []
                self.exclude_args[key] = self.exclude_args[key].append(value)


    def filter_complexity(self, rate):
        """Filters a specific rate of complexity out of the queryset."""
        self.general_action('filter', 'complexity__in', rate)

    #def exclude_complexity(self, rate):
    #    self.general_action('exclude', 'complexity__in', rate)


    def filter_nutrient_content(self, rate):
        """Filters a specific rate of nutrient content out of the queryset."""
        self.general_action('filter', 'nutrient_content__in', rate)

    #def exclude_nutrient_content(self, rate):
    #    self.general_action('exclude', 'nutrient_content__in', rate)


    def filter_duration(self, range_from, range_to):
        """Filters a specific range of duration out of the queryset."""
        self.general_action('filter', 'duration__range', (range_from, range_to))

    def filter_price(self, range_from, range_to):
        """Filters a specific range of price out of the queryset."""
        self.general_action('filter', 'price__range', (range_from, range_to))
        
    def filter_vegetarian(self, vegetarian):
        """Includes or excludes vegetarian meals into or from the queryset."""
        self.general_action('filter', 'vegetarian', vegetarian)
        
    def filter_vegan(self, vegan):
        """Includes or excludes vegan meals into or from the queryset."""
        self.general_action('filter', 'vegan', vegan)


    def get_queryset(self):
        """Applies all saved actions onto the queryset."""
        if self.queryset is not None:
            return self.queryset.exclude(**self.exclude_args).filter(**self.filter_args)
        else:
            return Meal.objects.exclude(**self.exclude_args).filter(**self.filter_args)