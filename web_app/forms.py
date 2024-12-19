from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Course, Attendance
from django.db.models import Q


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'person'
        if commit:
            user.save()
        return user

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Mantieni invariato il valore di user_type
        if self.instance.pk:  # L'utente esiste già (aggiornamento)
            user.user_type = self.instance.user_type
        if commit:
            user.save()
        return user


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'planned_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'effective_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

class UpdateAttendanceForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class SearchForm(forms.Form):
    course_n = forms.IntegerField(required=False, label="Numero Corso")
    course = forms.CharField(required=False, max_length=200, label="Nome Corso")
    year  = forms.ChoiceField(
        required=False,
        choices= [],
        label="Anno"
    )
    planned_date = forms.DateField(required=False)
    effective_date = forms.DateField(required=False)
    type = forms.ChoiceField(
        choices=[],
        required=False,
        label = "Tipo"
    )
    start = forms.CharField(required=False, max_length=200, label="Inizio")
    check_review = forms.CharField(required=False, max_length=200, label="Check Review")
    end = forms.CharField(required=False, max_length=200, label="Fine")
    duration = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label="Durata")
    i_e = forms.ChoiceField(
        required=False,
        choices=[],
        label="I/E"
    )
    trainer = forms.CharField(required=False, max_length=200, label="Trainer")
    cost = forms.DecimalField(required=False, max_digits=10, decimal_places=2, label="Costo")
    requirement = forms.CharField(required=False, max_length=200, label="Requisiti")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Serve str() perché se no fallisce "if form.year.value == value" nel template, siccome form.year.value è una stringa e year è un intero
        year_choices = [(str(year), year) for year in Course.objects.all().values_list("year", flat=True).distinct().order_by("-year").exclude(year__isnull=True)]
        self.fields['year'].choices = [("", "Tutti")] + year_choices

        type_choices = [(type, type) for type in Course.objects.all().values_list("type", flat=True).distinct().exclude(type__isnull=True)]
        self.fields['type'].choices = [("", "Tutti")] + type_choices

        i_e_choices = [(i_e, i_e) for i_e in Course.objects.all().values_list("i_e", flat=True).distinct().exclude(i_e__isnull=True)]
        self.fields['i_e'].choices = [("", "Tutti")] + i_e_choices


class CustomUserFilterForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(Q(user_type='person') | Q(user_type='quality_manager')),
        required=False,
        label="Seleziona Utente",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
