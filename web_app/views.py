from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserUpdateForm, TrainingPlanForm, UpdateRelazioneForm
from .models import CustomUser, TrainingPlan, Relazione


# Create your views here.

def home(request):
    return render(request, 'web_app/home.html', context={'title': 'Home', })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'

class CustomUserDetailView(DetailView):
    model = CustomUser
    template_name = 'web_app/user_detail.html'


class CustomUserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'web_app/user_update.html'
    form_class = CustomUserUpdateForm

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        request = self.request
        messages.success(request, 'Account modificato con successo!')
        return reverse("user_detail", kwargs={'pk': pk})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        request = self.request
        messages.success(request, 'Password modificata con successo!')
        return reverse("user_detail", kwargs={'pk': pk})


class TrainingPlansListView(ListView):
    model = TrainingPlan
    template_name = "web_app/training_plans_list.html"

    def get_queryset(self):
        return TrainingPlan.objects.order_by('-file_year')   # aggiungi course_n


def training_plan_detail(request, pk):
    training_plan = get_object_or_404(TrainingPlan, pk=pk)

    # Query per ottenere le relazioni associate al training plan
    relazioni = Relazione.objects.filter(training_plan=training_plan)

    # Suddivisione per stato
    pianificato = relazioni.filter(stato='pianificato').select_related('user')
    completato = relazioni.filter(stato='completato').select_related('user')

    context = {
        'training_plan': training_plan,
        'pianificato_users': [rel.user for rel in pianificato],
        'completato_users': [rel.user for rel in completato],
    }
    return render(request, 'web_app/training_plan_detail.html', context)


class TrainingPlanCreateView(CreateView):
    model = TrainingPlan
    form_class = TrainingPlanForm
    template_name = 'web_app/training_plan_create.html'


    def get_success_url(self):
        messages.success(self.request, 'Corso creato con successo!')
        return reverse('training_plans')


class TrainingPlanUpdateView(UpdateView):
    model = TrainingPlan
    form_class = TrainingPlanForm
    template_name = 'web_app/training_plan_update.html'

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        messages.success(self.request, 'Corso modificato con successo!')
        return reverse('training_plan_detail', kwargs={'pk': pk})


class TrainingPlanDeleteView(DeleteView):
    model = TrainingPlan
    template_name = 'web_app/training_plan_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Corso eliminato con successo!')
        return reverse('training_plans')


def planned_completed_update(request, pk):
    users = CustomUser.objects.filter(user_type='persona')

    training_plan = get_object_or_404(TrainingPlan, pk=pk)

    if request.path.__contains__('planned'):
        stato_corrente = 'pianificato'
    else:
        stato_corrente = 'completato'

    # Ottieni tutti gli utenti con lo stato corrente
    utenti_in_relazione = Relazione.objects.filter(
        training_plan=training_plan, stato=stato_corrente
    ).values_list('user_id', flat=True)

    if request.method == "POST":
        form = UpdateRelazioneForm(request.POST)
        if form.is_valid():
            # Ottieni gli utenti selezionati dal form
            users_selected = form.cleaned_data['users']

            # Aggiungi utenti nuovi (che non sono già in relazione)
            for user in users_selected:
                if not Relazione.objects.filter(
                    training_plan=training_plan, user=user, stato=stato_corrente
                ).exists():
                    Relazione.objects.create(
                        training_plan=training_plan, user=user, stato=stato_corrente
                    )

            # Rimuovi utenti deselezionati (che sono in relazione ma non nel form)
            for user_id in utenti_in_relazione:
                if user_id not in [user.id for user in users_selected]:
                    Relazione.objects.filter(
                        training_plan=training_plan, user_id=user_id, stato=stato_corrente
                    ).delete()

            messages.success(request, f'Utenti {stato_corrente} modificati con successo!')

            return redirect('training_plan_detail', pk=training_plan.pk)
    else:
        # Precompila il form con gli utenti selezionati
        form = UpdateRelazioneForm(initial={'users': utenti_in_relazione})

    return render(request, 'web_app/planned_completed_update.html', {'form': form, 'training_plan': training_plan, 'persone': users, 'title': f'Aggiorna {stato_corrente}'})