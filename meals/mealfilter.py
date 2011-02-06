from django.db.models import Avg, Max

from .models import Meal, EatenMeal, UserProfile
from .utils import recent_weeks, QuerysetFilter

class MealFilter(QuerysetFilter):
    def __init__(self, request=None, queryset=None):
        super(MealFilter, self).__init__(request, queryset, Meal)
        
    def exclude_often_eaten(self):
        """Excludes meals that the current user has eaten very often in the last three weeks."""
        # Get eaten meals that were eaten in the last three weeks by the current user
        user_profile = UserProfile.load_from_user(self._request.user)
        recent_eaten_meals = EatenMeal.objects.filter(user_profile=user_profile, last_time__range=recent_weeks())
        
        avg_times_eaten = recent_eaten_meals.aggregate(Avg('times'))['times__avg']
        max_times_eaten = recent_eaten_meals.aggregate(Max('times'))['times__max']
        
        # Calculating the average of the maximum times and average times of eaten meals,
        # to get a compromise between the imho too low normal average
        # and the too high maximum
        higher_avg = int((avg_times_eaten + max_times_eaten) / 2)
        
        # Filtering eaten meals that are lesser than the new average
        possible_eaten_meals = recent_eaten_meals.filter(times__lt=higher_avg)
        
        # Retrieving the meals that belong to the possible "eaten" meals
        possible_meals = possible_eaten_meals.get_meals()
        
        # Retrieving the meals that've not been eaten, i.e. there is no EatenMeal instance, yet
        all_eaten_meals = EatenMeal.objects.filter(user_profile=user_profile).get_meals()
        never_eaten_meals = Meal.objects.all() - all_eaten_meals
        
        # Meals that have already been eaten, but not in the last three weeks
        notrecent_eaten_meals = all_eaten_meals - recent_eaten_meals.get_meals()
        
        # We're not doing a second bitwise action with "|", because it would also
        # add never_eaten_meals that were not filtered by the general filters before
        self.bitwise_action('&', possible_meals | never_eaten_meals | notrecent_eaten_meals)

    def filter_type(self, type):
        """Filters by a specific meal type."""
        self.general_action('filter', 'type', type)
        
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