from django import forms
from .models import Ticket
from django_ckeditor_5.widgets import CKEditor5Widget


class TicketForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditor5Widget(), required=False)

    class Meta:
        model = Ticket
        # fields = '__all__'
        exclude = ('author', )

