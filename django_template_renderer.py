from django.template import Engine, Context, Template
from django.conf import settings
from django.shortcuts import render

settings.configure()

def render_template(template_string, context_dictionary):
    """
    Renders a django template
    Input:
        template_string - str. The template to render.
        context_dictionary - dict. The dictionary to use to render the template.
    Output:
        str. The template string rendered.
    Example:
        >>> render_template('{% if x %}{{x}}{% else %}x is falsey{% endif %}', {'x': 5})
        '5'
        >>> render_template('{% if x %}{{x}}{% else %}x is falsey{% endif %}', {'x': 0})
        'x is falsey'
    """
    engine = Engine()
    template = Template(template_string)
    ctx = Context(context_dictionary)
    return template.render(ctx)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
