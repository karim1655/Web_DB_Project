from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser


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
        pk = self.get_context_data()["object"].pk
        return reverse("user_detail", kwargs={'pk': pk})