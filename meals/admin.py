from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import MealType, Meal


class MealAdmin(admin.ModelAdmin):
    list_display = ('title', 'complexity', 'duration', 'nutrient_content', 'vegetarian', 'vegan', 'price', 'type',)
    list_filter = ('complexity', 'nutrient_content', 'vegetarian', 'vegan', 'type',)
    search_fields = ('title', 'notes',)
    ordering = ('title',)

class MealTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'position',)
    list_filter = ('position',)
    search_fields = ('title',)
    ordering = ('position',)

admin.site.register(Meal, MealAdmin)
admin.site.register(MealType, MealTypeAdmin)