from django.template import Engine, Context, Template
from django.conf import settings
from django.shortcuts import render

settings.configure()

def render_template(template_string, context_dictionary):
    engine = Engine()
    template = Template(template_string)
    ctx = Context(context_dictionary)
    return template.render(ctx)
