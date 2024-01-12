from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from transactions.models import Transaction
from django.core.mail import EmailMessage,EmailMultiAlternatives


def send_transaction_email(user,subject, template):
        message = render_to_string(template, {
            'user' : user,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class UserRegistrationView(FormView):
    template_name = 'accounts/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form) # form_valid function call hobe jodi sob thik thake
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})

class ChangePassWord(PasswordChangeView):
    template_name = 'accounts/changepassword.html'
    success_url = reverse_lazy('profile')
    def form_valid(self,form):
        response = super().form_valid(form)
        messages.success(
                self.request,
                f"Your Password Successfully Changed")
        send_transaction_email(self.request.user, "Change Password", "transactions/deposite_email.html")
        return super().form_valid(form)