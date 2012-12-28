#coding=utf-8
'''
Created on 04/09/2012

@author: Johnny
'''
from ckeditor.widgets import CKEditorWidget
from portfolio.models import Cliente,Servico, Trabalho, CaracteristicaServico
from custom_admin import custom_admin
from custom_admin.custom_model_admin import CustomModelAdmin
from django import forms

class CaracteristicaServicoAdmin(CustomModelAdmin):
    list_display = ('descricao',)
    search_fields = ['descricao']    
    exclude = ['slug']

class ServicoForm(forms.ModelForm):
    descricao = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Servico

class ServicosAdmin(CustomModelAdmin):
    list_display = ('imagem_icone','titulo','intro',)
    list_display_links = ('titulo','intro',)
    search_fields = ['titulo','intro','descricao']
    list_filter = ['caracteristicas']
    exclude = ['slug']
    form = ServicoForm

class ClientesAdmin(CustomModelAdmin):
    list_display = ('imagem','descricao','site')
    search_fields = ['site','descricao']
    exclude = ['slug']


class TrabalhoForm(forms.Form):
    descricao = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Trabalho

class TrabalhoAdmin(CustomModelAdmin):
    list_display = ('titulo','descricao_pequena','servico','cliente')
    search_fields = ['titulo']
    list_filter = ['servico']
    exclude = ['slug']


custom_admin.custom_site.register(Cliente,ClientesAdmin)
custom_admin.custom_site.register(CaracteristicaServico,CaracteristicaServicoAdmin)
custom_admin.custom_site.register(Servico,ServicosAdmin)
custom_admin.custom_site.register(Trabalho,TrabalhoAdmin)
