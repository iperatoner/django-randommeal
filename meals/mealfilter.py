from .models import Meal

class QuerysetFilter(object):
    def __init__(self, queryset=None, model=None):
        self._model = model
        self._queryset = queryset
        self._exclude_args = {}
        self._filter_args = {}
        
    def general_action(self, action, model_field, value):
        """
        Executes a general action, like filtering or excluding
        specific stuff (`value`) on a specific field
        (`model_field`, also including django's magic `__in` and `__range` stuff)
        """
        assert action in ['filter', 'exclude']
        if action == 'filter':
            self._filter_args[model_field] = value
        elif action == 'exclude':
            self._exclude_args[model_field] = value

    def bind(self, queryset=None, model=None):
        """Binds a Queryset and/or a Model class to the Filter."""
        if queryset is not None:
            self._queryset = queryset
        if model is not None:
            self._model = model
        
    def execute(self):
        """Applies all saved actions onto the queryset."""
        if self._queryset is not None:
            return self._queryset.filter(**self._filter_args)
        else:
            return self._model.objects.filter(**self._filter_args)


class MealFilter(QuerysetFilter):
    def __init__(self, queryset=None):
        super(MealFilter, self).__init__(queryset, Meal)

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