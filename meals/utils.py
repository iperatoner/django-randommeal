import math
import random
from datetime import datetime, timedelta

from django.template import RequestContext, loader
from django.http import HttpResponse
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

def recent_weeks():
    """
    Returns a tuple of two datetime instances:
    The beginning of the day 3 weeks before today and the end of today.
    """
    now = datetime.now()
    today_start = datetime.min.replace(year=now.year, month=now.month, day=now.day)
    today_end = (today_start + timedelta(days=1)) - timedelta.resolution
    three_weeks_before = today_start - timedelta(weeks=3)
    return (three_weeks_before, today_end)


class JSONResponse(HttpResponse):
    def __init__(self, json_dict):
        HttpResponse.__init__(self, json.dumps(json_dict), mimetype='application/json')
        

class QuerysetFilter(object):
    def __init__(self, request=None, queryset=None, model=None):
        self._request = request
        self._model = model
        self._queryset = queryset
        self._resulting_queryset = queryset
        
        self._exclude_args = {}
        self._filter_args = {}
        self._bitwise_operations = {'&': [], '|': []}
        
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
    
    def bitwise_action(self, operator, queryset):
        assert operator in ['&', '|']
        if operator == '&':
            self._bitwise_operations['&'].append(queryset)
        elif operator == '|':
            self._bitwise_operations['|'].append(queryset)

    def bind(self, queryset=None, model=None):
        """Binds a Queryset and/or a Model class to the Filter."""
        if queryset is not None:
            self._queryset = queryset
        if model is not None:
            self._model = model
    
    def execute_general(self):
        """Applies all saved general actions onto the queryset."""
        if self._queryset is not None:
            self._resulting_queryset = self._queryset.filter(**self._filter_args)
        else:
            self._resulting_queryset =  self._model.objects.filter(**self._filter_args)
    
    def execute_bitwise(self):
        """Executes all saved bitwise operations onto the queryset."""
        assert self._resulting_queryset is not None
        
        for bwo_and in self._bitwise_operations['&']:
            resulting_qs = self._resulting_queryset & bwo_and
        for bwo_or in self._bitwise_operations['|']:
            resulting_qs = self._resulting_queryset | bwo_or
        
        # Only use the new queryset if it contains anything
        if len(resulting_qs) > 0:
            self._resulting_queryset = resulting_qs
            
    def execute(self):
        """Applies all saved actions (general and bitwise) onto the queryset."""
        self.execute_general()
        self.execute_bitwise()
        return self._resulting_queryset
