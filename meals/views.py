import random
import math

from .models import MealType, Meal, EatenMeal, UserProfile
from .mealfilter import MealFilter
from .utils import render_template, JSONResponse

def index(request):
    return render_template(request, 'meals/index.html')

def generate(request):
    grouped_meals = []
    mealtypes = MealType.objects.all().order_by('position')
    for mt in mealtypes:
        possible_meals = Meal.objects.filter(type=mt)
        
        # TODO: Apply filters
        
        # Generating a random index to then being able to select a random item from the list
        meal_index = int(math.ceil(random.random() * len(possible_meals))) - 1
        assert meal_index <= len(possible_meals) - 1
        meal = possible_meals[meal_index]
        
        # Adding a group of mealtype + randomly generated meals to the list
        grouped_meals.append({
            'type': mt,
            'meal': meal
        })
    
    if request.is_ajax():
        return JSONResponse({
            'grouped_meals': grouped_meals
        })
    else:
        return render_template(request, 'meals/result.html',
            grouped_meals=grouped_meals
        )