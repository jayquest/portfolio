#coding=utf-8
'''
Created on 04/09/2012

@author: Johnny
'''
from ckeditor.widgets import CKEditorWidget
from django.conf.urls import patterns, url
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.templatetags.static import static
import views
from portfolio.models import *
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


    def configuracoes_servicos_view(self,request):
        import forms
        from string import capitalize
        from django.utils.encoding import force_unicode
        from django.contrib.admin import  helpers

        model = self.model
        opts = model._meta
        prepopuled_fields = {}

        add, change = True,False

        if request.method == 'POST': # If the form has been submitted...

            form = forms.ConfigServicoForm(request.POST,request.FILES) # A form bound to the POST data

            if request.POST.has_key('_update'):
                form.fields['imagem'].required = False

            if form.is_valid(): # All validation rules pass

                form.fields['imagem'].required = True

                try:
                    texto = TextoPagina.objects.get(slug='texto_servico')
                except:
                    texto = TextoPagina()

                if texto.texto == None or texto.texto != form.cleaned_data['texto']:
                    texto.texto = form.cleaned_data['texto']

                if not request.POST.has_key('_update') or request.FILES.has_key('imagem'):
                    texto.imagem = request.FILES['imagem']



                texto.slug = 'texto_servico'
                texto.save()

                form = forms.ConfigServicoForm()
                form.initial['texto']  = texto.texto
                form.initial['imagem'] = texto.imagem

                change = True
                add = False
        else:
            form = forms.ConfigServicoForm()
            try:
                texto = TextoPagina.objects.get(slug='texto_servico')
                change = True
                add = False
                form.initial['texto']  = texto.texto
                form.initial['imagem'] = texto.imagem
            except:
                pass

        adminForm = helpers.AdminForm(form,[('Texto da página de serviços',{'fields':['imagem','texto']})],prepopuled_fields)

        media = self.media + adminForm.media

        return render_to_response('admin/config_form.html',
            {
                'add':add,
                'change':change,
                'title': 'Configurações',
                'is_popup': "_popup" in request.REQUEST,
                'show_delete': False,
                'has_delete_permission':False,
                'has_add_permission':True,
                'has_change_permission':True,
                'errors': form.errors,
                'app_label': opts.app_label,
                'current_app':capitalize(opts.app_label),
                'all_app_list':self.admin_site.all_app_list(request),
                'module_name': force_unicode(opts.verbose_name_plural),
                'opts':opts,
                'has_file_field':True,
                'adminform':adminForm,
                'save_as':False,
                'media':media,
            }
            ,context_instance=RequestContext(request))

    def get_urls(self):
        urls = super(ServicosAdmin, self).get_urls()
        info = self.model._meta.app_label, self.model._meta.module_name
        my_urls = patterns('',
                   url(r'^config/$', custom_admin.custom_site.admin_view(self.configuracoes_servicos_view),name='%s_%s_config' % info),
            )
        return my_urls + urls

    @property
    def media(self):
        super_media = super(ServicosAdmin, self).media

        js = [
            'cufon-yui.js',
            'TitilliumText.font.js',
            'cufon-replace-ckeditor.js',
            ]

        current_media = forms.Media(js=[static('js/%s' % url) for url in js])

        media = super_media + current_media

        return media

    def get_model_perms(self, request):
        permiss = super(ServicosAdmin, self).get_model_perms(request)
        permiss['config'] = self.has_change_permission(request) and self.has_add_permission(request)
        return permiss

class ClientesAdmin(CustomModelAdmin):
    list_display = ('imagem_icone','descricao','site')
    list_display_links = ('descricao',)
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
