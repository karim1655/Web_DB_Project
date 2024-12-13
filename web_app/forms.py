from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, TrainingPlan, Relazione


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'user_type', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].label = "Registrati come"


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_type'].label = "Cambia ruolo"

class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = '__all__'
        widgets = {
            'planned_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'effective_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
