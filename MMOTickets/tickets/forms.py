from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Ticket


class TicketForm(forms.ModelForm):
    """Form for comments to the article."""
    # content = forms.CharField(widget=CKEditor5Widget())
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["body"].required = False
    #
    # class Meta:
    #     model = Ticket
    #     fields = ("body")
    #     # widgets = {
    #     #         "body": CKEditor5Widget(
    #     #         attrs={"class": "django_ckeditor_5"}, config_name="comment")
    #     #     }
    class Meta:
        model = Ticket
        fields = '__all__'


# class PostAdmin(admin.ModelAdmin):
#     form = TicketForm
#
# admin.site.register(Ticket, PostAdmin)