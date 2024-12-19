from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from functools import wraps
from django.contrib.auth.decorators import user_passes_test

from .models import CustomUser


# Decorator per le FBV
#Controlla sia che lo user sia autenticato, sia che sia un quality manager
def quality_manager_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'quality_manager':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Accesso riservato ai Quality Manager")
    return _wrapped_view

# Decoratore per consentire l'accesso solo al superuser
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


# Mixin per le CBV
#Controlla sia che lo user sia autenticato, sia che sia un quality manager
class QualityManagerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        current_user = get_object_or_404(CustomUser, id=request.user.id)
        if request.user.is_authenticated and current_user.user_type == 'quality_manager':
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("Accesso riservato ai Quality Manager")