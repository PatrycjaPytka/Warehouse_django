from django.http import HttpResponse, JsonResponse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect, reverse
from django.views.generic import View

from magazine_main.models import Item, Borrowed, ItemType
from magazine_main.forms import EditItemForm, EditUserForm, BorrowItemForm, AddItemForm, AddItemTypeForm,EditItemTypeForm


class ManageWarehouseView(LoginRequiredMixin, View):
    template_name = "magazine_main/manage_warehouse.html"
    context = {}

    def get(self, request):
        self.context["borrow_item_form"] = BorrowItemForm()
        self.context["add_item_form"] = AddItemForm()
        self.context["add_item_type_form"] = AddItemTypeForm()
        return render(request, self.template_name, context=self.context)

    def post(self, request):
        if 'action_add_user' in request.POST:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
                if 'is_admin' in request.POST:
                    user.is_superuser = True
                user.save()
                messages.success(request, _('User successfully created'))
            except IntegrityError:
                messages.error(request, _('User with provided username already exists'))
            return redirect('magazine_main:manage_warehouse')
        
        elif 'action_add_item' in request.POST:
            try:
                type_obj = get_object_or_404(ItemType, pk=request.POST['type'])
                Item.objects.create(type=type_obj, name=request.POST['name'], serial_number=request.POST['serial_number'])
                messages.success(request, _('Item successfully created'))
            except Exception:
                messages.error(request, _('Something went wrong. Please try again'))
            return redirect('magazine_main:manage_warehouse')

        elif 'action_add_item_type' in request.POST:
            try:
                ItemType.objects.create(name=request.POST['name'])
                messages.success(request, _('Item type successfully created'))
            except Exception:
                messages.error(request, _('Something went wrong. Please try again'))
            return redirect('magazine_main:manage_warehouse')

        elif 'action_borrow_item' in request.POST:
            try:
                user_obj = get_object_or_404(User, id=request.POST['user'])
                item_obj = get_object_or_404(Item, id=request.POST['item'])
                Borrowed.objects.create(user=user_obj, item=item_obj, amount=int(request.POST['amount']))
                item_obj.borrowed = True
                item_obj.save()
                messages.success(request, _('Item successfully borrowed'))
            except Exception:
                messages.error(request, _('Something went wrong. Please try again'))
            return redirect('magazine_main:manage_warehouse')

class ManageWarehouseAction(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.GET_ACTIONS = {
            'get_item_type': self.get_item_type,
            'get_item': self.get_item,
            'get_user': self.get_user,
            'delete_user_borrowed': self.delete_user_borrowed,
        }

        self.POST_ACTIONS = {
            'edit_item_type': self.edit_item_type,
            'edit_item': self.edit_item,
            'edit_user': self.edit_user,
            'delete_item': self.delete_item,
            'delete_user': self.delete_user,
            }
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk, action):
        if 'item_type' in action:
            self.item_type_obj = get_object_or_404(ItemType, pk=pk)
        elif 'item' in action:
            self.item_obj = get_object_or_404(Item, pk=pk)
        elif 'borrowed' in action:
            self.user_borrowed_obj = get_object_or_404(Borrowed, pk=pk)
        else:
            self.user_obj = get_object_or_404(User, pk=pk)
        if action in self.GET_ACTIONS:
            return self.GET_ACTIONS[action](request)
        return redirect('magazine_main:manage_warehouse')
    
    def post(self, request, pk, action):
        if 'user' in action:
            self.user_obj = get_object_or_404(User, pk=pk)
        elif 'item_type' in action: 
            self.item_type_obj = get_object_or_404(ItemType, pk=pk)
        else: 
            self.item_obj = get_object_or_404(Item, pk=pk)
        if action in self.POST_ACTIONS:
            return self.POST_ACTIONS[action](request)
        return redirect('magazine_main:manage_warehouse')        

    def get_item_type(self, _):
        item_type_edit_form = EditItemTypeForm(instance=self.item_type_obj)
        return HttpResponse(item_type_edit_form.as_p())

    def get_item(self, _):
        item_edit_form = EditItemForm(instance=self.item_obj)
        return HttpResponse(item_edit_form.as_p())

    def get_user(self, _):
        user_edit_form = EditUserForm(instance=self.user_obj)
        return HttpResponse(user_edit_form.as_p())

    def edit_item_type(self, request):
        form = EditItemTypeForm(request.POST, instance=self.item_type_obj)
        if form.is_valid():
            form.save()
            messages.success(request, _('Item type successfully edited'))
        return redirect('magazine_main:manage_warehouse')          

    def edit_item(self, request):
        form = EditItemForm(request.POST, instance=self.item_obj)
        if form.is_valid():
            form.save()
            messages.success(request, _('Item successfully edited'))
        return redirect('magazine_main:manage_warehouse')    
    
    def edit_user(self, request):
        form = EditUserForm(request.POST, instance=self.user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, _('User successfully edited'))
        return redirect('magazine_main:manage_warehouse') 

    def delete_item(self, request):
        try:
            self.item_obj.delete()
            messages.success(request, _('Item successfully deleted'))
        except ProtectedError:
            messages.error(request, _(f'You cannot delete this item because some users does not returned it yet.'))
        except Exception as e:
            messages.error(request, _(f'Something went wrong. {e}'))
        return redirect('magazine_main:manage_warehouse')

    def delete_user(self, request):
        try:
            self.user_obj.delete()
            messages.success(request, _('User successfully deleted'))
        except ProtectedError:
            messages.error(request, _(f'You cannot delete this user because he did not return all borrowed items yet.'))
        except Exception as e:
            messages.error(request, _(f'Something went wrong. {e}'))
        return redirect('magazine_main:manage_warehouse')

    def delete_user_borrowed(self, request):
        try:
            self.user_borrowed_obj.delete()
            messages.success(request, _('Borrowed item successfully deleted'))
        except Exception as e:
            messages.error(request, _(f'Something went wrong. {e}'))
        return redirect('magazine_main:manage_warehouse')


class ItemTypesList(LoginRequiredMixin, BaseDatatableView):
    model = ItemType
    columns = ['name', 'amount', 'amount_left', '']
    order_columns = ['name', 'amount', 'amount_left', '']

    def get_initial_queryset(self):
        return ItemType.objects.all().order_by('created_at')

    def render_buttons(self, id):
        buttons = f'''<button class="editItemTypeBtn btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#editItemTypeModal" data-id="{id}"> Edit </button> 
                      <button class="deleteItemTypeBtn btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#deleteItemTypeModal" data-id="{id}"> Delete </button>'''
        return buttons

    def render_column(self, row, column):
        if column == '':
            return self.render_buttons(row.id)
        return super(ItemTypesList, self).render_column(row, column)
    
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(name__istartswith=search)
        return qs        


class ItemsList(LoginRequiredMixin, BaseDatatableView):
    model = Item
    columns = ['type.name', 'name', 'serial_number', '']
    order_columns = ['type.name', 'name', 'serial_number', '']

    def get_initial_queryset(self):
        return Item.objects.all().order_by('created_at')

    def render_buttons(self, id):
        buttons = f'''<button class="editItemBtn btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#editItemModal" data-id="{id}"> Edit </button> 
                      <button class="deleteItemBtn btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#deleteItemModal" data-id="{id}"> Delete </button>'''
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


class UsersList(LoginRequiredMixin, BaseDatatableView):
    model = User
    columns = ['username', 'is_admin', 'borrowed_items', '']
    order_columns = ['username', 'is_admin', 'borrowed_items', '']

    def get_initial_queryset(self):
        return User.objects.all().order_by('id')

    def render_buttons(self, id, row_type):
        if row_type == 'borrowed_list':
            buttons = f'<button class="borrowedListBtn btn btn-outline-dark" data-bs-toggle="modal" data-bs-target="#borrowedUserModal" data-id="{id}"> Borrowed items </button>'
        else:
            buttons = f'''<button class="editUserBtn btn btn-outline-warning" data-bs-toggle="modal" data-bs-target="#editUserModal" data-id="{id}"> Edit </button> 
                        <button class="deleteUserBtn btn btn-outline-danger" data-bs-toggle="modal" data-bs-target="#deleteUserModal" data-id="{id}"> Delete </button>'''
        return buttons

    def render_column(self, row, column):
        if column == 'is_admin':
            if get_object_or_404(User, id=row.id).is_superuser:
                return '<i class="fa-solid fa-circle-check"></i>'
            else:
                return '<i class="fa-solid fa-circle-minus"></i>'
        if column == '':
            return self.render_buttons(row.id, row_type='actions')
        if column == 'borrowed_items':
            user = get_object_or_404(User, id=row.id)
            return self.render_buttons(row.id, 'borrowed_list')
        return super(UsersList, self).render_column(row, column)
    
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(username__istartswith=search)
        return qs  


class BorrowedUserList(LoginRequiredMixin, BaseDatatableView):
    model = Borrowed
    columns = ['item.name', 'amount', '']
    order_columns = ['item.name', 'amount', '']

    def get_initial_queryset(self):
        return Borrowed.objects.filter(user__id=self.kwargs.get('pk'))

    def render_buttons(self, id):
        url = reverse('magazine_main:manage_action', kwargs={'pk': id, 'action': 'delete_user_borrowed'})
        return f'<a href={url} class="btn btn-outline-danger"> Delete </a>'

    def render_column(self, row, column):
        if column == '':
            return self.render_buttons(row.id)
        return super(BorrowedUserList, self).render_column(row, column)
    
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(item__name__istartswith=search)
        return qs  
    