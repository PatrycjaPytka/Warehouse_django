from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View

from magazine_main.models import Borrowed


class ManageWarehouseView(LoginRequiredMixin, View):
    template_name = "magazine_main/manage_warehouse.html"
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)
