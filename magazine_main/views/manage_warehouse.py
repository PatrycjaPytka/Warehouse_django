from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.views.generic import View

from magazine_main.models import Item


class ManageWarehouseView(LoginRequiredMixin, View):
    template_name = "magazine_main/manage_warehouse.html"
    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        if 'action_add_user' in request.POST:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            except IntegrityError:
                messages.error(request, _('User with provided username already exists'))
            if 'is_admin' in request.POST:
                user.is_superuser = True
            user.save()
            messages.success(request, _('User successfully created'))
        
        elif 'action_add_item' in request.POST:
            print(request.POST)
            try:
                Item.objects.create(name=request.POST['name'], amount=int(request.POST['amount']), amount_left=int(request.POST['amount']))
            except Exception:
                messages.error(request, _('Something went wrong. Please try again'))
            messages.success(request, _('Item successfully created'))
        return redirect('magazine_main:manage_warehouse')


class ItemsList(LoginRequiredMixin, BaseDatatableView):
    model = Item
    columns = ['name', 'amount', 'amount_left', '']
    order_columns = ['name', 'amount', 'amount_left', '']

    def get_initial_queryset(self):
        return Item.objects.all().order_by('created_at')

    def render_buttons(self, id):
        print(id)
        buttons = f'''<button class="btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#editItemModal"> Edit </button> 
                      <button class="btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#deleteItemModal"> Delete </button>'''
        return buttons

    def render_column(self, row, column):
        if column == '':
            return self.render_buttons(row.id)
        return super(ItemsList, self).render_column(row, column)
    
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)
        return qs        