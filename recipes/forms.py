from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'cooking_time', ]
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }
