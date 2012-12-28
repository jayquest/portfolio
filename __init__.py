from django.conf import settings

settings.TEMPLATE_CONTEXT_PROCESSORS += ("portfolio.views.servicos_list",)