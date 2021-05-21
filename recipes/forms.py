from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    tags = forms.ChoiceField(required=False)
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'description', 'cooking_time', 'tags']
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
        }
