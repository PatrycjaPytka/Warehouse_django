from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from magazine_main.models import Borrowed


@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class IndexView(LoginRequiredMixin, ListView):
    model = Borrowed
    paginate_by = 50
