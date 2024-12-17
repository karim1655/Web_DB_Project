from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, CustomUserUpdateForm, CourseForm, UpdateAttendanceForm, SearchForm
from .models import CustomUser, Course, Attendance, File
from .decorators import quality_manager_required, QualityManagerRequiredMixin


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        planned = Course.objects.filter(courses_attendances__user=request.user, courses_attendances__state="planned").order_by('-effective_date', '-planned_date')
        completed = Course.objects.filter(courses_attendances__user=request.user, courses_attendances__state="completed").order_by('-effective_date', '-planned_date')
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

    files = File.objects.filter(user_id=request.user.id, course=pk).order_by('-uploaded_at')

    # Query per ottenere le attendances associate al corso
    attendances = Attendance.objects.filter(course_id=pk)
    # Suddivisione per state
    planned = attendances.filter(state='planned').select_related('user')
    completed = attendances.filter(state='completed').select_related('user')

    # Attendances dell'utente corrente per questo corso, per poterle rimuovere se vuole
    current_user_planned = attendances.filter(state='planned', user_id=request.user.id).first()
    current_user_completed = attendances.filter(state='completed', user_id=request.user.id).first()

    context = {
        'course': course,
        'planned_users': [attendance.user for attendance in planned],
        'completed_users': [attendance.user for attendance in completed],
        'files': files,
        'current_user_planned': current_user_planned,
        'current_user_completed': current_user_completed,
    }
    return render(request, 'web_app/course_detail.html', context)


class CourseCreateView(QualityManagerRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'web_app/course_create.html'


    def get_success_url(self):
        messages.success(self.request, 'Corso creato con successo!')
        return reverse('courses')


class CourseUpdateView(QualityManagerRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'web_app/course_update.html'

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        messages.success(self.request, 'Corso modificato con successo!')
        return reverse('course_detail', kwargs={'pk': pk})


class CourseDeleteView(QualityManagerRequiredMixin, DeleteView):
    model = Course
    template_name = 'web_app/course_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Corso eliminato con successo!')
        return reverse('courses')

@quality_manager_required
def planned_completed_update(request, pk):
    users = CustomUser.objects.filter(Q(user_type='person') | Q(user_type='quality_manager'))

    course = get_object_or_404(Course, pk=pk)

    if request.path.__contains__('planned'):
        current_state = 'planned'
        stato = 'Pianificato'
    else:
        current_state = 'completed'
        stato = 'Completato'

    # Ottieni tutti gli utenti con lo state corrente
    users_in_attendance = Attendance.objects.filter(
        course=course, state=current_state
    ).values_list('user_id', flat=True)

    if request.method == "POST":
        form = UpdateAttendanceForm(request.POST)
        if form.is_valid():
            # Ottieni gli utenti selezionati dal form
            users_selected = form.cleaned_data['users']

            # Aggiungi utenti nuovi (che non sono già in attendance)
            for user in users_selected:
                if not Attendance.objects.filter(
                    course=course, user=user, state=current_state
                ).exists():
                    Attendance.objects.create(
                        course=course, user=user, state=current_state
                    )

            # Rimuovi utenti deselezionati (che sono in attendance ma non nel form)
            for user_id in users_in_attendance:
                if user_id not in [user.id for user in users_selected]:
                    Attendance.objects.filter(
                        course=course, user_id=user_id, state=current_state
                    ).delete()

            messages.success(request, f'Utenti {current_state} modificati con successo!')

            return redirect('course_detail', pk=course.pk)
    else:
        # Precompila il form con gli utenti selezionati
        form = UpdateAttendanceForm(initial={'users': users_in_attendance})

    return render(request, 'web_app/planned_completed_update.html', {'form': form, 'course': course, 'persone': users, 'title': f'Aggiorna {stato}'})


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

@login_required
def upload_file(request, pk):
    if request.method == 'POST' and request.FILES.get('uploaded_file'):
        uploaded_file = request.FILES['uploaded_file']
        File.objects.create(user_id=request.user.id, course_id=pk, file=uploaded_file)
        messages.success(request, 'File caricato con successo!')
    return redirect('course_detail', pk=pk)

@login_required
def delete_file(request, pk, file_id):
    if request.method == "POST":
        file_instance = get_object_or_404(File, id=file_id)

        if file_instance.user != request.user:
            return HttpResponseForbidden("Non sei autorizzato a eliminare questo file.")

        file_instance.file.delete(save=False)  # Rimuove il file dal filesystem
        file_instance.delete()  # Rimuove la entry dal database

        messages.success(request, "File eliminato con successo.")
        return redirect('course_detail', pk)


@login_required
def add_planned_or_completed_attendance(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = get_object_or_404(CustomUser, id=request.user.id)

    if request.path.__contains__('planned'):
        if Attendance.objects.filter(course=course, user=user, state='planned').exists():
            messages.warning(request, "Hai già una presenza pianificata per questo corso.")
        else:
            Attendance.objects.create(course=course, user=user, state='planned')
            messages.success(request, "Presenza pianificata aggiunta con successo!")
    elif request.path.__contains__('completed'):
        if Attendance.objects.filter(course=course, user=user, state='completed').exists():
            messages.warning(request, "Hai già una presenza completata per questo corso.")
        else:
            Attendance.objects.create(course=course, user=user, state='completed')
            messages.success(request, "Presenza completata aggiunta con successo!")

    return redirect('course_detail', pk=course.id)


@login_required
def remove_planned_or_completed_attendance(request, course_id, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)

    if attendance_id == -1:
        messages.warning('Non si può rimuovere una presenza che non esiste')

    attendance.delete()

    if request.path.__contains__('planned'):
        messages.success(request, "Presenza pianificata rimossa con successo!")
    else:
        messages.success(request, "Presenza completata rimossa con successo!")

    return redirect('course_detail', pk=course_id)
