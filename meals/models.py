from django.db import models

class MealType(models.Model):
    title = models.CharField(_('Title'), help_text=_("Title of the type of meal."), max_length=32)
    position = models.IntegerField(_('Position on day'), help_text=_("The position of this meal on a day."))

class Meal(models.Model):
    type = models.ForeignKey(MealType, verbose_name=_("Meal type"), help_text=_("The type of this meal (e.g. breakfast)."))
    title = models.CharField(_("Title"), help_text=_("The title or name of this meal."), max_length=128)
    notes = models.TextField(_("Notes"), help_text=_("Notes or a description of this meal."))
    complexity = models.IntegerField(_("Complexity"), help_text=_("How complex is it to prepare this meal?")) # TODO: select options
    duration = models.IntegerField(_("Duration"), help_text=_("How much time will it approximately take to prepare this meal?")) # in minutes
    nutrient_content = models.IntegerField(_("Nutrient content"), help_text=_("How nutritious is that meal?"))
    vegetarian = models.BooleanField(_("Vegetarian?"), help_text=_("Is this meal suitable for vegetarian people?"))
    vegan = models.BooleanField(_("Vegan?"), help_text=_("Is this meal suitable for vegan people?"))
    price = models.IntegerField(_("Approximate price"), help_text=_("How much will it probably cost to prepare this meal?"))
