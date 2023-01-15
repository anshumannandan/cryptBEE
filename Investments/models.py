from django.db.models.base import Model
from django.db.models.fields import FloatField, CharField, URLField, TextField
from django.db.models.fields.related import OneToOneField
from django.db.models import CASCADE
from Authentication.models import User
from django.core.validators import RegexValidator


class Coin(Model):
    Name = CharField(max_length=10, unique=True)
    FullName = CharField(max_length=100, unique=True)
    Price = FloatField(null=True, blank=True)
    ChangePct = FloatField(null=True, blank=True)
    Image = URLField()
    Description = TextField()

    def __str__(self):
        return '%s : %s' % (self.Name, self.Price)

    class Meta:
        ordering = ['Name']


class PAN_Verification(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='pan_details')
    pan_number = CharField(unique=True, max_length=10,
                           validators=[RegexValidator(regex='[A-Z]{5}[0-9]{4}[A-Z]{1}', message='Invalid PAN',),])