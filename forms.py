from ckeditor.widgets import CKEditorWidget
from django import forms

__author__ = 'Jonatas'


class ConfigServicoForm(forms.Form):
    imagem = forms.ImageField()
    texto = forms.CharField(widget=CKEditorWidget())

