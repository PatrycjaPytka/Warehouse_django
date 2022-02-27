from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from magazine_main.models import Borrowed


class IndexView(LoginRequiredMixin, ListView):
    model = Borrowed
    paginate_by = 50
