# from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from toolkit.aboelela.process import process
from .forms import FileFieldForm
# from wsgiref.util import FileWrapper


class IndexView(TemplateView):
    template_name = "main/index.html"


class AboelelaView(FormView):
    form_class = FileFieldForm
    template_name = "aboelela/aboelela.html"
    success_url = "."
    extra_context = {'file': None}

    def form_valid(self, form):
        files = form.cleaned_data["files_to_process"]
        processed_file = process(files)
        print(processed_file.open('rb'))

        print("Processed file:", processed_file.content)
        return FileResponse(processed_file, as_attachment=True,
                            filename=processed_file.name)
