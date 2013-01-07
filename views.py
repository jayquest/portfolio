#coding=utf-8
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import Form
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from portfolio.models import *

def servicos_list(request):
    return {'lista_servicos':Servico.objects.order_by('?').all()[:5]}

def clientes_list(request):
    return {'lista_clientes':Cliente.objects.order_by('?').all()[:6]}

def index(request,pagina):
    work_list = Trabalho.objects.all()

    paginator = Paginator(work_list,9)

    try:
        lista = paginator.page(pagina)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lista = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lista = paginator.page(paginator.num_pages)

    servicos = []

    for l in lista:
        if not(servicos.__contains__(l.servico)):
            servicos.append(l.servico)

    tags = []

    for l in lista:
        for t in l.tags.all():
            if not(tags.__contains__(t)):
                tags.append(t)

    return render_to_response('portfolio.html',{'trabalhos':lista,'servicos':servicos,'tags':tags},context_instance=RequestContext(request))

def trabalho(request,slug):

    try:
        trabalho = Trabalho.objects.get(slug=slug)

        try:
            next = Trabalho.objects.get(id=trabalho.id+1)
        except:
            next = None
        try:
            prev = next_produto = Trabalho.objects.get(id=trabalho.id-1)
        except:
            prev = None
    except ObjectDoesNotExist:
        raise Http404

    return render_to_response('portfolio-item.html',{'trabalho':trabalho,'proximo':next,'anterior':prev},context_instance=RequestContext(request))

def clientes(request,pagina):
    client_list = Cliente.objects.all()

    paginator = Paginator(client_list,8)

    try:
        lista = paginator.page(pagina)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        lista = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        lista = paginator.page(paginator.num_pages)

    return render_to_response('clients.html',{'clientes':lista,'current':'clientes'},context_instance=RequestContext(request))

def servicos(request):
    servicos = Servico.objects.all()
    try:
        texto_servicos = TextoPagina.objects.get(slug='texto_servico')
    except:
        texto_servicos = None

    return render_to_response('services.html',{'servicos':servicos,'texto_servico':texto_servicos},context_instance=RequestContext(request))

def detalhes_servicos(request,servico):
    try:
        service = Servico.objects.get(slug=servico)
    except ObjectDoesNotExist:
        raise Http404

    return render_to_response('service_detail.html',{'servico':service},context_instance=RequestContext(request))


