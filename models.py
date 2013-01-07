#coding=utf-8
from django.core.validators import MaxLengthValidator
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager

from django.db import models

# Create your models here.

class CaracteristicaServico(models.Model):
    descricao = models.CharField(max_length=40)
    slug = models.SlugField(max_length=100)

    def __unicode__(self):
        return self.descricao

class Servico(models.Model):
    titulo = models.CharField(max_length=50)
    intro = models.TextField(validators=[MaxLengthValidator(250)])
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='servicos/imagens')
    slug = models.SlugField(max_length=100)
    caracteristicas = models.ManyToManyField(CaracteristicaServico)

    def __unicode__(self):
        return self.titulo

    def imagem_icone(self):
        return  mark_safe(u'<img src="%s" style="height:48px"/>' % self.imagem.url)
    imagem_icone.short_description = 'Imagem'
    imagem_icone.allow_tags = True

class Cliente(models.Model):
    descricao = models.CharField(max_length=100)
    site = models.URLField(null=True,blank=True,help_text='Endereço do site do cliente')
    imagem = models.ImageField(upload_to='clientes')
    slug = models.SlugField(max_length=100)

    def __unicode__(self):
        return self.descricao

    def imagem_icone(self):
        return  mark_safe(u'<img src="%s" style="height:48px"/>' % self.imagem.url)
    imagem_icone.short_description = 'Imagem'
    imagem_icone.allow_tags = True

class Trabalho(models.Model):
    titulo = models.CharField(max_length=40)
    descricao_pequena = models.CharField(max_length=80)
    descricao = models.TextField()
    servico = models.ForeignKey(Servico)
    cliente = models.ForeignKey(Cliente)
    imagem = models.ImageField(upload_to='trabalhos',null=True,blank=True)
    video = models.CharField(max_length=450,null=True,blank=True,help_text='Link do video (youtube) ')
    tags = TaggableManager(help_text='')
    slug = models.SlugField(max_length=160)

class TextoPagina(models.Model):
    titulo = models.CharField(max_length=100,null=True,blank=True)
    texto = models.TextField()
    imagem = models.ImageField(upload_to='textos/',blank=True,null=True)
    slug = models.SlugField(max_length=120)



from django.db.models import signals
from django.template.defaultfilters import slugify
from portfolio.models import Trabalho,Cliente,Servico,CaracteristicaServico

def cliente_pre_save(signal,instance,sender, **kwargs):
    slug = slugify(instance.descricao)
    novo_slug = slug
    contador = 0

    while Cliente.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

def caracteristica_servico_pre_save(signal,instance,sender, **kwargs):
    slug = slugify(instance.descricao)
    novo_slug = slug
    contador = 0

    while CaracteristicaServico.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

def servico_pre_save(signal,instance,sender, **kwargs):
    slug = slugify(instance.titulo)
    novo_slug = slug
    contador = 0

    while Servico.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

def trabalho_pre_save(signal,instance,sender, **kwargs):
    slug = slugify(instance.titulo)
    novo_slug = slug
    contador = 0

    while Trabalho.objects.filter(slug=novo_slug).exclude(id=instance.id).count() > 0:
        contador += 1
        novo_slug = '%s-%d'%(slug, contador)

    instance.slug = novo_slug

signals.pre_save.connect(caracteristica_servico_pre_save,sender=CaracteristicaServico)
signals.pre_save.connect(servico_pre_save,sender=Servico)
signals.pre_save.connect(cliente_pre_save,sender=Cliente)
signals.pre_save.connect(trabalho_pre_save,sender=Trabalho)
