import math
import random

from django.template import RequestContext, loader
from django.http import HttpResponse, Http404
from django.utils import simplejson as json
from django.shortcuts import get_object_or_404

from .models import Meal, MealType
from . import settings as meals_settings

def sequence_to_int(seq):
    """Converts elements of a sequence to integers."""
    if type(seq) is tuple:
        return (int(x) for x in seq)
    elif type(seq) is list:
        return [int(x) for x in seq]
    
def render_template(request, template, mimetype=None, **kwargs):  
    """  
    `render_to_response` sucks. `render_template` takes template-locals as
    keyword arguments, not as a dict as positional argument.
    """  
    context_processor = RequestContext(request)
    return HttpResponse( 
        loader.render_to_string(template, kwargs, context_processor),
        mimetype=mimetype
    )
    
def get_random_item(queryset):
    """Randomly selects an item from a Django queryset."""
    index = int(math.ceil(random.random() * len(queryset))) - 1
    assert index >= 0
    return queryset[index]

def get_range_field_value(form, pair_field, custom_from_field, custom_to_field, values_to_int=True):
    """
    Returns the value of a range form field, which allows static ranges as well as custom ones.
    
    `form` is the form to get the field value from,
    `pair_field` is the name of the field with a predefined range pair, e.g. "4-13"
    `custom_from_field` is the name of the custom range field to get the minimum value from, e.g. "4"
    `custom_to_field` is the name of the custom range field to get the maximum value from, e.g. "13"
    `values_to_int` wether to convert all range values to an integer
    """
    if form.cleaned_data[pair_field] == meals_settings.CUSTOM_VALUE:
        range = (form.cleaned_data[custom_from_field], form.cleaned_data[custom_to_field])
    else:
        range = form.cleaned_data[pair_field].split(meals_settings.DELIMITER)
    if values_to_int:
        range = [int(x) for x in range]
    return range

def urlencode_grouped_meals(grouped_meals):
    """
    Creates a dump of grouped meals (item: type + meal) for use in url query strings.
    Return format: 'meals=type_id:meal_id [...]'
    Example: 'meals=1:1,2:3,3:6,4:2'
    """
    grouped_meals_urlencoded = 'grouped_meals='
    for group in grouped_meals:
        grouped_meals_urlencoded += str(group['type'].id) + ':' + str(group['meal'].id) + ','
    return grouped_meals_urlencoded[:-1]

def urldecode_grouped_meals(grouped_meals_urlencoded):
    """
    Decodes a url-dump of grouped meals (item: type + meal)
    to be able to fetch the objects for the template.
    """
    grouped_meals = []
    groups = grouped_meals_urlencoded.split(',')
    for group in groups:
        type_id, meal_id = group.split(':')
        type = get_object_or_404(MealType, id=type_id)
        meal = get_object_or_404(Meal, id=meal_id)
        grouped_meals.append({
            'type': type,
            'meal': meal
        })
    return grouped_meals


class JSONResponse(HttpResponse):
    def __init__(self, json_dict):
        HttpResponse.__init__(self, json.dumps(json_dict), mimetype='application/json')
