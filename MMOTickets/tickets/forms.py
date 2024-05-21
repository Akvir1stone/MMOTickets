from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Ticket


class TicketForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditor5Widget(), required=False)

    class Meta:
        model = Ticket
        # fields = '__all__'
        exclude = ('author', )


# class PostAdmin(admin.ModelAdmin):
#     form = TicketForm
#
# admin.site.register(Ticket, PostAdmin)
