from django.forms import ModelForm
from .models import TwitterUser

class TwitterForm(ModelForm):
    class Meta:
        model = TwitterUser
        fields = ['username']