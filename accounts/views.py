from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView
from accounts.forms import MyUserCreationForm
from accounts.forms.user_creation_form import UserChangeForm

User = get_user_model()


class RegisterView(CreateView):
    template_name = "user_create.html"
    model = User
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next = self.request.GET.get('next')
        if not next:
            next = self.request.POST.get('next')
        if not next:
            next = reverse("webapp:index")
        return next


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user_obj'


class UserChangeView(PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def has_permission(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.object.pk})



class UserPasswordChangeView(PermissionRequiredMixin, PasswordChangeView):
    template_name = 'user_password_change.html'

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.request.user.pk})

    def has_permission(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user == self.request.user
