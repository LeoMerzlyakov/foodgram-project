from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    tags_error = forms.IntegerField(required=False)
    ingr_error = forms.IntegerField(required=False)
    class Meta:
        model = Recipe
        fields = [
            'title',
            'image',
            'description',
            'cooking_time',
            'tags_error',
            'ingr_error'
        ]
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }
