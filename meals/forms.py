from django import forms
from . import settings as meals_settings

filter_onoff_attrs = {'class': 'filter-onoff'}

class MealFilterForm(forms.Form):
    # Duration
    filter_duration = forms.BooleanField(widget=forms.CheckboxInput(attrs=filter_onoff_attrs), required=False)
    duration_pair = forms.ChoiceField(
        choices=meals_settings.DURATION_CHOICES,
        required=False
    )
    custom_duration_from = forms.IntegerField(max_value=999, required=False)
    custom_duration_to = forms.IntegerField(max_value=999, required=False)
    
    # Price
    filter_price = forms.BooleanField(widget=forms.CheckboxInput(attrs=filter_onoff_attrs), required=False)
    price_pair = forms.ChoiceField(
        choices=meals_settings.PRICE_CHOICES,
        required=False
    )
    custom_price_from = forms.IntegerField(max_value=999, required=False)
    custom_price_to = forms.IntegerField(max_value=999, required=False)
    
    # Complexity
    filter_complexity = forms.BooleanField(widget=forms.CheckboxInput(attrs=filter_onoff_attrs), required=False)
    complexity_levels = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=meals_settings.LEVEL_CHOICES_FORM,
        required=False
    )
    
    # Nutrient content
    filter_nutrient_content = forms.BooleanField(widget=forms.CheckboxInput(attrs=filter_onoff_attrs), required=False)
    nutrient_content_levels = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=meals_settings.LEVEL_CHOICES_FORM,
        required=False
    )
    
    # Vegetarian
    vegetarian = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=meals_settings.VEG_CHOICES,
        required=False,
        initial=meals_settings.VEG_BOTH
    )
    
    # Vegan
    vegan = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=meals_settings.VEG_CHOICES,
        required=False,
        initial=meals_settings.VEG_BOTH
    )