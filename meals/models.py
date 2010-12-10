from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from . import settings as meals_settings

class MealType(models.Model):
    """Model representing a single type of meal (e.g. breakfast)."""
    
    title = models.CharField(_("Title"), help_text=_("Title of the type of meal."), max_length=32)
    position = models.IntegerField(_("Position on day"), help_text=_("The position of this meal on a day."))
    
    def __unicode__(self):
        return self.title


class Meal(models.Model):
    """Model representing a meal of any type."""
    
    type = models.ForeignKey(MealType, verbose_name=_("Meal type"), help_text=_("The type of this meal (e.g. breakfast)."))
    title = models.CharField(_("Title"), help_text=_("The title or name of this meal."), max_length=128)
    notes = models.TextField(_("Notes"), help_text=_("Notes or a description of this meal."))
    
    complexity = models.IntegerField(_("Complexity"), help_text=_("How complex is it to prepare this meal?"), choices=meals_settings.LEVEL_CHOICES)
    duration = models.IntegerField(_("Duration"), help_text=_("How much time will it approximately take to prepare this meal?")) # in minutes
    nutrient_content = models.IntegerField(_("Nutrient content"), help_text=_("How nutritious is that meal?"), choices=meals_settings.LEVEL_CHOICES)
    vegetarian = models.BooleanField(_("Vegetarian?"), help_text=_("Is this meal suitable for vegetarian people?"))
    vegan = models.BooleanField(_("Vegan?"), help_text=_("Is this meal suitable for vegan people?"))
    price = models.IntegerField(_("Approximate price"), help_text=_("How much will it probably cost to prepare this meal?"))
    
    def __unicode__(self):
        return "%s: %s" % (self.type.title, self.title)


class EatenMeal(models.Model):
    """Model representing a meal that a user ate at least one time."""
    
    user_profile = models.ForeignKey('UserProfile')
    meal = models.ForeignKey(Meal, verbose_name=_("Meal"))
    times = models.IntegerField(_("How often?"))
    last_time = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return "%s: %d %s" % (self.user_profile.user.name, self.times, self.meal.title)


class UserProfile(models.Model):
    """Model representing a user profile, e.g. holding eaten meals."""
    
    user = models.ForeignKey(User, unique=True)
    eaten_meals = models.ManyToManyField(Meal, through=EatenMeal)

    def __unicode__(self):
        return "%s\'s profile" % self.user.username