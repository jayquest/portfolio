#coding=utf-8
'''
Created on 05/09/2012

@author: Johnny
'''

from django.conf.urls import patterns, url


urlpatterns = patterns('portfolio.views',
    # Examples:
    url(r'^trabalho/(?P<slug>[a-zA-Z0-9_.-]+)', 'trabalho', name='trabalho'),
#    url(r'^servicos/', 'servicos', name='servicos'),
#    url(r'^servicos/ver/(?P<servico>[a-zA-Z0-9_.-]+)', 'detalhes_servicos', name='detalhar_servico'),
    url(r'^(?P<pagina>\d{1,2})?', 'index', name='portfolio'),
#    url(r'^clientes/', 'clientes', name='clientes'),

)
