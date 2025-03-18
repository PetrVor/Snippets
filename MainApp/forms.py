from django.forms import ModelForm, ValidationError, TextInput,Textarea
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
       model = Snippet
       # Описываем поля, которые будем заполнять в форме
       fields = ['name', 'lang', 'code']
       labels = {"name": "", "lang": "", "code":""}
       widgets = {
           "name" : TextInput(attrs = {"placeholder": "sneppet name"}),
           "code" : Textarea(attrs = {"placeholder": "sneppet code"}),
       }

    def clean_name(self):
        snippet_name = self.cleaned_data.get("name")
        if len(snippet_name) > 3:
            return snippet_name
        raise ValidationError("snippet is too short")
           
