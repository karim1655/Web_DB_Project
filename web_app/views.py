from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserUpdateForm, CourseForm, UpdateRelazioneForm, SearchForm
from .models import CustomUser, Course, Relazione


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        planned = Course.objects.filter(corsi_relazione__user=request.user, corsi_relazione__stato="pianificato").order_by('-effective_date', '-planned_date')
        completed = Course.objects.filter(corsi_relazione__user=request.user, corsi_relazione__stato="completato").order_by('-effective_date', '-planned_date')
    else:
        planned = None
        completed = None
    #print(planned)
    #print(completed)
    return render(request, 'web_app/home.html', context={'title': 'Home', 'planned': planned, 'completed': completed})


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


class CoursesListView(ListView):
    model = Course
    template_name = "web_app/courses_list.html"

    def get_queryset(self):
        return Course.objects.order_by('-year', '-effective_date', '-planned_date')


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    # Query per ottenere le relazioni associate al training plan
    relazioni = Relazione.objects.filter(course=course)

    # Suddivisione per stato
    pianificato = relazioni.filter(stato='pianificato').select_related('user')
    completato = relazioni.filter(stato='completato').select_related('user')

    context = {
        'course': course,
        'pianificato_users': [rel.user for rel in pianificato],
        'completato_users': [rel.user for rel in completato],
    }
    return render(request, 'web_app/course_detail.html', context)


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'web_app/course_create.html'


    def get_success_url(self):
        messages.success(self.request, 'Corso creato con successo!')
        return reverse('courses')


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'web_app/course_update.html'

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        messages.success(self.request, 'Corso modificato con successo!')
        return reverse('course_detail', kwargs={'pk': pk})


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'web_app/course_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Corso eliminato con successo!')
        return reverse('courses')


def planned_completed_update(request, pk):
    users = CustomUser.objects.filter(user_type='persona')

    course = get_object_or_404(Course, pk=pk)

    if request.path.__contains__('planned'):
        stato_corrente = 'pianificato'
    else:
        stato_corrente = 'completato'

    # Ottieni tutti gli utenti con lo stato corrente
    utenti_in_relazione = Relazione.objects.filter(
        course=course, stato=stato_corrente
    ).values_list('user_id', flat=True)

    if request.method == "POST":
        form = UpdateRelazioneForm(request.POST)
        if form.is_valid():
            # Ottieni gli utenti selezionati dal form
            users_selected = form.cleaned_data['users']

            # Aggiungi utenti nuovi (che non sono già in relazione)
            for user in users_selected:
                if not Relazione.objects.filter(
                    course=course, user=user, stato=stato_corrente
                ).exists():
                    Relazione.objects.create(
                        course=course, user=user, stato=stato_corrente
                    )

            # Rimuovi utenti deselezionati (che sono in relazione ma non nel form)
            for user_id in utenti_in_relazione:
                if user_id not in [user.id for user in users_selected]:
                    Relazione.objects.filter(
                        course=course, user_id=user_id, stato=stato_corrente
                    ).delete()

            messages.success(request, f'Utenti {stato_corrente} modificati con successo!')

            return redirect('course_detail', pk=course.pk)
    else:
        # Precompila il form con gli utenti selezionati
        form = UpdateRelazioneForm(initial={'users': utenti_in_relazione})

    return render(request, 'web_app/planned_completed_update.html', {'form': form, 'course': course, 'persone': users, 'title': f'Aggiorna {stato_corrente}'})


def search(request):
    ctx = None

    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            course_n = form.cleaned_data.get("course_n")
            course_name = form.cleaned_data.get("course_name")
            year = form.cleaned_data.get("year")
            planned_date = form.cleaned_data.get("planned_date")
            effective_date = form.cleaned_data.get("effective_date")
            type = form.cleaned_data.get("type")
            start = form.cleaned_data.get("start")
            check_review = form.cleaned_data.get("check_review")
            end = form.cleaned_data.get("end")
            duration = form.cleaned_data.get("duration")
            i_e = form.cleaned_data.get("i_e")
            trainer = form.cleaned_data.get("trainer")
            cost = form.cleaned_data.get("cost")
            requirement = form.cleaned_data.get("requirement")

            courses = Course.objects.all()
            if course_n:
                courses = courses.filter(course_n__iexact=course_n)
            if course_name:
                courses = courses.filter(course_name__icontains=course_name)
            if year:
                courses = courses.filter(year__iexact=year)
            if planned_date:
                courses = courses.filter(planned_date__date=planned_date)
            if effective_date:
                courses = courses.filter(effective_date__date=effective_date)
            if type:
                courses = courses.filter(type__iexact=type)
            if start:
                courses = courses.filter(start__icontains=start)
            if check_review:
                courses = courses.filter(check_review__icontains=check_review)
            if end:
                courses = courses.filter(end__icontains=end)
            if duration:
                courses = courses.filter(duration__lte=duration)
            if i_e:
                courses = courses.filter(i_e__iexact=i_e)
            if trainer:
                courses = courses.filter(trainer__icontains=trainer)
            if cost:
                courses = courses.filter(cost__lte=cost)
            if requirement:
                courses = courses.filter(requirement__icontains=requirement)

            courses = courses.order_by('-year', '-effective_date', '-planned_date')

            ctx = {
                'form': form,
                'courses': courses,
            }

    return render(request, 'web_app/search.html', ctx)