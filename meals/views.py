from .models import MealType, Meal, EatenMeal, UserProfile
from .mealfilter import MealFilter
from .utils import render_template, get_random_item, JSONResponse

def index(request):
    return render_template(request, 'meals/index.html')

def generate(request):
    grouped_meals = []
    mealtypes = MealType.objects.all().order_by('position')
    for mt in mealtypes:
        possible_meals = Meal.objects.filter(type=mt)
        
        # TODO: Apply filters
        # Duration:         Range (Select box with predefined range, resp. Input boxes: duration_from, duration_to)
        # Price:            Range (Select box with predefined range, resp. Input boxes: price_from, price_to)
        # Complexity:       Integer list (Check boxes: low[yes|no], med[yes|no], high[yes|no])
        # Nutrient content: Integer list (Check boxes: low[yes|no], med[yes|no], high[yes|no])
        # Vegetarian:       Boolean (Check box: vegetarian[yes|no])
        # Vegan:            Boolean (Check box: vegetarian[yes|no])
        
        meal = get_random_item(possible_meals)
        
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