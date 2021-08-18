from jinja2 import Template
import os

def render(template_name, folder='templates', **kwargs):
    file_path = os.path.join(folder, template_name)

    with open(file_path, encoding='utf-8') as template:
        template_to_render = Template(template.read())
    return template_to_render.render(**kwargs)
