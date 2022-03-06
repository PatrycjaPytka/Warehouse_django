from xml.dom.minidom import CharacterData
from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=100)
    amount = models.PositiveSmallIntegerField(default=0)
    amount_left = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Borrowed(models.Model):
    class Meta:
        verbose_name_plural = "Borrowed"
        ordering = ['-id']
    user = models.ForeignKey(User, related_name='borrowed_by', on_delete=models.PROTECT)
    item = models.ForeignKey(Item, related_name='borrowed_item', on_delete=models.PROTECT)
    amount = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name - self.amount}'

