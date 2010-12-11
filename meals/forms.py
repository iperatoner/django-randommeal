from django import forms
from . import settings as meals_settings

class MealFilterForm(forms.Form):
    # Duration
    duration_pair = forms.ChoiceField(
        choices=meals_settings.DURATION_CHOICES,
        required=False
    )
    custom_duration_from = forms.IntegerField(max_value=999, required=False)
    custom_duration_to = forms.IntegerField(max_value=999, required=False)
    
    # Price
    price_pair = forms.ChoiceField(
        choices=meals_settings.PRICE_CHOICES,
        required=False
    )
    custom_price_from = forms.IntegerField(max_value=999, required=False)
    custom_price_to = forms.IntegerField(max_value=999, required=False)
    
    # Complexity
    include_complexity_groups = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=meals_settings.LEVEL_CHOICES,
        required=False
    )
    
    # Nutrient content
    include_nutrient_content_groups = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=meals_settings.LEVEL_CHOICES,
        required=False
    )
    
    # Vegetarian
    vegetarian = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=meals_settings.VEG_CHOICES,
        required=False
    )
    
    # Vegan
    vegan = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=meals_settings.VEG_CHOICES,
        required=False
    )