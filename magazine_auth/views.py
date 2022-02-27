from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext as _
from django.views.generic import View

from .forms import RegisterForm


class LoginView(View):
    template_name = 'magazine_auth/login.html'
    context = {}

    def get(self, request):
        self.context['register_form'] = RegisterForm()
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        print(request.POST)
        if 'login_submit' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            print(username, password, user)
            if user is not None:
                login(request, user)
                return redirect('magazine_main:index')
            else:
                messages.error(request, _('Provided data is invalid'))

        elif 'register_submit' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password'])
                    form.save()
                    messages.success(request, _('Account successfully created. You can login now'))
                except Exception as e:
                    print(e)
                    messages.error(request, _('Something went wrong'))
            else:
                for error, message in form.errors.items():
                    messages.error(request, _(str(message)))
        else:
            messages.error(request, _('Provided data is invalid'))

        return redirect('magazine_auth:auth')


def logout_view(request):
    logout(request)