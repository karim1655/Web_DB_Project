from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserUpdateForm
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
    template_name = "web_app/trainingplans_list.html"

    def get_queryset(self):
        return TrainingPlan.objects.order_by('-file_year')   # aggiungi course_n