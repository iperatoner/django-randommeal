from .models import MealType, Meal, EatenMeal, UserProfile
from .mealfilter import MealFilter
from .forms import MealFilterForm
from .utils import sequence_to_int, render_template, get_random_item, get_range_field_value, JSONResponse
from . import settings as meals_settings

def index(request):
    form = MealFilterForm(request.POST or None)
    return render_template(request, 'meals/index.html', filterform=form)

def generate(request):
    form = MealFilterForm(request.POST or None)
    
    if form.is_valid():
        mealfilter = MealFilter()
        
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
        
        # A list of type+meal dicts
        grouped_meals = []
        
        # Going through all available mealtypes and randomly select a meal of it
        mealtypes = MealType.objects.all().order_by('position')
        for mt in mealtypes:
            # Getting queryset by meal type and binding it to the mealfilter
            possible_meals = Meal.objects.filter(type=mt)
            mealfilter.bind(possible_meals)
            
            # Execute the applied filters
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
        
        if request.is_ajax():
            return JSONResponse({'grouped_meals': grouped_meals})
        else:
            return render_template(request, 'meals/result.html',
                grouped_meals=grouped_meals
            )
    else:
        return index(request)