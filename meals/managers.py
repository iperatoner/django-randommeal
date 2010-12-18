from django.db import models as django_models
from django.db.models.query import QuerySet

import models


class EatenMealQuerySet(QuerySet):
    def get_meals(self):
        """Returns the meals that are included in the eaten meals of this queryset."""
        meal_ids = []
        for eaten_meal in self:
            meal_ids.append(eaten_meal.meal.id)
        return models.Meal.objects.filter(id__in=meal_ids)

class EatenMealManager(django_models.Manager):
    def get_query_set(self):
        return EatenMealQuerySet(self.model)

class MealQuerySet(QuerySet):
    def add_or_sub(self, operator, other):
        assert operator in ['+', '-']
        if operator == '+':
            result = set(self) | set(other)
        elif operator == '-':
            result = set(self) - set(other)
            
        meal_ids = []
        for meal in result:
            meal_ids.append(meal.id)
        return self.model.objects.filter(id__in=meal_ids)
    
    def __add__(self, other):
        """Adds the meals of `other` from this queryset."""
        return self.add_or_sub('+', other)
    
    def __sub__(self, other):
        """Removes the meals of `other` from this queryset."""
        return self.add_or_sub('-', other)

class MealManager(django_models.Manager):
    def get_query_set(self):
        return MealQuerySet(self.model)