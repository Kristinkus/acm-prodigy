from django.shortcuts import redirect
from django.views.generic import CreateView, View
from django.contrib.auth.views import LoginView

from config.settings import RECAPTCHA_PUBLIC_KEY
from main.forms import AuthUserForm, CreateUserForm
from main.mixins import LanguageMixin
from main.utils import Configuration
from volunteers.forms import VolunteerForm
from volunteers.models import Volunteer



class IndexView(LanguageMixin, View):
    template_name = 'volunteers/index.html'

    def get(self, request, *args, **kwargs):
        form = None
        if Volunteer.objects.filter(user=request.user).exists():
            form = VolunteerForm(instance=request.user.volunteer)
        else:
            form = VolunteerForm()

        return self.render_page(
            request,
            self.template_name,
            {
                'form': form,
            }
        )

    def post(self, request, *args, **kwargs):
        form = VolunteerForm(request.POST, instance=request.user.volunteer)
        if form.is_valid():
            form.save()
            return redirect('volunteers-index')

        return self.render_page(
            request,
            self.template_name,
            {
                'form': form,
            }
        )


def create_volunteer(request):
    if not request.method == 'POST' or\
       not request.user.is_authenticated or \
       Volunteer.objects.filter(user=request.user).exists():
        return redirect('volunteers-index')

    Volunteer.objects.create(user=request.user)
    return redirect('volunteers-index')


class SignUpView(LanguageMixin, CreateView):
    form_class = CreateUserForm
    success_url = 'volunteers-login'
    template_name = 'volunteers/registration/signup.html'

    def get(self, request, *args, **kwargs):
        agreement = Configuration('configuration.agreement')
        agreement_url = Configuration('configuration.agreement.url')

        return self.render_page(request, self.template_name, {
            'signup' : 'active',
            'captcha_key' : RECAPTCHA_PUBLIC_KEY,
            'form': self.get_form(),
            'agreement': agreement,
            'agreement_url': agreement_url,
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        agreement = Configuration('configuration.agreement')
        agreement_url = Configuration('configuration.agreement.url')

        if form.is_valid():
            if (
                Configuration('configuration.agreement') == 'true' and
                not form.cleaned_data['personal_data_agreement']
            ):
                form.add_error('personal_data_agreement', 'Required field')
            else:
                res = form.save()
                Volunteer.objects.create(user=res)
                return redirect(self.success_url)

        return self.render_page(
            request,
            self.template_name,
            {
                'form': form,
                'disable_footer': True,
                'agreement': agreement,
                'agreement_url': agreement_url,
            }
        )


class UserLoginView(LanguageMixin, LoginView):
    form_class = AuthUserForm
    template_name = 'volunteers/registration/login.html'

    def get(self, request, *args, **kwargs):
        return self.render_page(
            request,
            self.template_name,
            {
                'form': self.get_form(),
                'login': 'active',
            }
        )

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)