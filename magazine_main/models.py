from xml.dom.minidom import CharacterData
from django.db import models
from django.contrib.auth.models import User


class ItemType(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.amount}'

    @property
    def amount(self):
        return Item.objects.filter(type=self.id).count()

    @property
    def amount_left(self):
        return Item.objects.filter(type=self.id, borrowed=False).count()

class Item(models.Model):
    type = models.ForeignKey(ItemType, related_name='item_type', on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=300, unique=True)
    borrowed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.type.name} - {self.name} - {self.serial_number}'

class Borrowed(models.Model):
    class Meta:
        verbose_name_plural = "Borrowed"
        ordering = ['-id']
    user = models.ForeignKey(User, related_name='borrowed_by', on_delete=models.PROTECT)
    item = models.ForeignKey(Item, related_name='borrowed_item', on_delete=models.PROTECT)
    amount = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item.name} - {self.amount}'
