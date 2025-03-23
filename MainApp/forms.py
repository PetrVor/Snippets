from django.forms import CharField, ModelForm, PasswordInput, ValidationError, TextInput,Textarea
from MainApp.models import Comment, Snippet
from django.contrib.auth.models import User


class SnippetForm(ModelForm):
    class Meta:
       model = Snippet
       # Описываем поля, которые будем заполнять в форме
       fields = ['name', 'lang', 'code', 'public']
       labels = {"name": "", "lang": "", "code": "", "public": ""}
       widgets = {
           "name" : TextInput(attrs = {"placeholder": "sneppet name"}),
           "code" : Textarea(attrs = {"placeholder": "sneppet code"}),
       }

    def clean_name(self):
        snippet_name = self.cleaned_data.get("name")
        if len(snippet_name) > 3:
            return snippet_name
        raise ValidationError("snippet is too short")
    
class UserRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    password1 = CharField(label="password", widget = PasswordInput)
    password2 = CharField(label="password confirm", widget = PasswordInput)  

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) > 3:
            return username
        raise ValidationError("Username too short") 

    def clean_password2(self):
        pass1 = self.cleaned_data.get("password1") 
        pass2 = self.cleaned_data.get("password2")
        if pass1 and pass2 and pass1 == pass2:
            return pass2
        raise ValidationError("пароли не совпадают или пустые")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user    
    
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]    
        labels = {"text": "" }
        widgets =  {
            "text": Textarea(attrs={"placeholder" : "Комментарий для сниппета"})
        }
