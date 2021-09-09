from .render import render
from patterns.structure_patterns import Debug
import sys

sys.path.append("..")


class TemplateView:
    template_name = ''
    queryset = {}

    def get_context_data(self):
        return {}

    def render_template_with_context(self):
        template_name = self.template_name
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request=None):
        return self.render_template_with_context()


class ListView(TemplateView):

    def get_queryset(self):
        return self.queryset

    def get_context_data(self):
        context = self.queryset
        return context

class CreateView(TemplateView):

    def get_context_data(self):
        context = self.queryset
        return context

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context()
        else:
            return super().__call__(request)