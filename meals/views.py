from datetime import datetime

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404 
from django.contrib.auth.decorators import login_required
 
from .models import MealType, Meal
from .mealfilter import MealFilter
from .forms import MealFilterForm
from .utils import sequence_to_int, render_template, get_random_item, get_range_field_value
from .utils import urlencode_grouped_meals, urldecode_grouped_meals, get_eaten_meal, JSONResponse


def index(request):
    form = MealFilterForm(request.POST or None)
    return render_template(request, 'meals/index.html', filterform=form)

def generate(request):
    # If there is no grouped_meals dump in the url, just randomly generate the meals as usual
    if not request.GET.get('grouped_meals'):
        form = MealFilterForm(request.POST or request.GET or None)
        
        if form.is_valid():
            mealfilter = MealFilter(request)
            
            # Applying the selected filters
            
            if form.cleaned_data['filter_duration']:
                duration_range = get_range_field_value(form, 'duration_pair', 'custom_duration_from', 'custom_duration_to')
                mealfilter.filter_duration(duration_range)
                
            if form.cleaned_data['filter_price']:
                price_range = get_range_field_value(form, 'price_pair', 'custom_price_from', 'custom_price_to')
                mealfilter.filter_price(price_range)
                
            if form.cleaned_data['filter_complexity']:
                complexity_levels = sequence_to_int(form.cleaned_data['complexity_levels'])
                mealfilter.filter_complexity(complexity_levels)
                
            if form.cleaned_data['filter_nutrient_content']:
                nc_levels = sequence_to_int(form.cleaned_data['nutrient_content_levels'])
                mealfilter.filter_nutrient_content(nc_levels)
                
            if form.cleaned_data['vegetarian'] in ['0', '1']:
                vegetarian = bool(int(form.cleaned_data['vegetarian']))
                mealfilter.filter_vegetarian(vegetarian)
                
            if form.cleaned_data['vegan'] in ['0', '1']:
                vegan = bool(int(form.cleaned_data['vegan']))
                mealfilter.filter_vegan(vegan)
            
            if form.cleaned_data['exclude_often_eaten']:
                mealfilter.exclude_often_eaten()
            
            # A list of type+meal dicts
            grouped_meals = []
            
            # Going through all available mealtypes and randomly select a meal of each of them
            mealtypes = MealType.objects.all().order_by('position')
            for mt in mealtypes:
                mealfilter.filter_type(mt)
                
                # Execute all applied filters
                possible_meals = mealfilter.execute()
                
                # Wether there were matches or not
                if possible_meals:
                    meal = get_random_item(possible_meals)
                else:
                    meal = None
                
                # Adding a group of mealtype + randomly generated meals to the list
                grouped_meals.append({
                    'type': mt,
                    'meal': meal
                })
            
            # Generates a dump of the grouped meals for use in urls
            # (which is needed to save the randomly generated meals
            #  before hitting "have eaten" to be able to reuse the generated meals)
            grouped_meals_urlencoded = urlencode_grouped_meals(grouped_meals)
        else:
            return index(request)
    # Using the urldump of grouped meals
    else:
        grouped_meals_urlencoded = 'grouped_meals=' + str(request.GET.get('grouped_meals'))
        grouped_meals = urldecode_grouped_meals(request.GET.get('grouped_meals'))
        form = False
    
    if request.is_ajax():
        return JSONResponse({
            'grouped_meals': grouped_meals,
            'grouped_meals_urlencoded': grouped_meals_urlencoded
        })
    else:
        return render_template(request, 'meals/result.html',
            grouped_meals=grouped_meals,
            grouped_meals_urlencoded=grouped_meals_urlencoded,
            form=form
        )
        
def all_meals(request):
    mealtypes = MealType.objects.all().order_by('position')
    return render_template(request, 'meals/all.html', mealtypes=mealtypes)
        
def print_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    
    return render_template(request, 'meals/print-meal.html',
        meal=meal
    )

@login_required
def have_eaten(request, meal_id, redirect):
    meal = get_object_or_404(Meal, id=meal_id)
    
    # Get the proper EatenMeal-instance
    eaten_meal = get_eaten_meal(request.user, meal)
    
    if eaten_meal.times is not None:
        eaten_meal.times += 1
    else:
        eaten_meal.times = 1
    eaten_meal.last_time = datetime.now()
    eaten_meal.save()
    
    if not request.is_ajax() and redirect == 'result':
        return HttpResponseRedirect(reverse('rdm_generate') + '?' + request.GET.urlencode())
    elif redirect == 'all':
        return HttpResponseRedirect(reverse('rdm_all'))