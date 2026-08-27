from django import forms
from .models import Skill, Category


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('title', 'description', 'category', 'location', 'contact_info', 'image', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Freelance Logo Design'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6,
                                                   'placeholder': 'Describe what you offer, your experience, and what makes you a great fit...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Nairobi, Kenya (or Remote)'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email, phone, or preferred contact'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select a category"


class SkillSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title or keyword...'
        })
    )
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.all(),
        to_field_name='slug',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
