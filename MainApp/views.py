from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.forms import SnippetForm, UserRegistrationForm,CommentForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
            'pagename': 'Мои сниппеты',
            'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)


@login_required(login_url='home')
def add_snippet_page(request):
# Create empty form by GET method
    if request.method == "GET":
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета',
                'form': form
                }
        return render(request, 'pages/add_snippet.html', context)

# Getting data from the form and creating snippet based on them
    if request.method =="POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets-list")
        return render(request,"pages/add_snippet.html", {'form': form})    


def snippets_page(request):
    snippets = Snippet.objects.filter(public=True)
    context = {
            'pagename': 'Просмотр сниппетов',
            'snippets': snippets,
            "count": snippets.count(),}
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id):
    context ={'pagename': 'просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:    
        return render(request,"pages/error.html", context | {"error" : f"Snippet with id:{snippet_id} not found!"}) 
    else:
        comments_form = CommentForm      
        context['snippet'] = snippet
        context["type"] = "view"
        context["comments_form"] = comments_form
    return render(request,'pages/snippet_page.html', context)

@login_required
def snippet_edit(request,snippet_id):
    context ={'pagename': 'Редактирование сниппета'}
    try:
        snippet = Snippet.objects.filter(user=request.user).get(id=snippet_id)
    except ObjectDoesNotExist: 
        return Http404
    # Getting page with snippet data
    if request.method == "GET":
        form = SnippetForm()
        context = {
                    "snippet": snippet,
                    "type": "edit",
                }
        return render(request, 'pages/snippet_page.html', context)

    # Getting data from the form and creating snippet based on them
    if request.method =="POST":
        data_form =request.POST
        snippet.name = data_form["name"]
        snippet.code = data_form["code"]
        snippet.public = data_form.get("public", False)
        snippet.save()      
        return redirect("snippets-list")
  

@login_required
def snippet_delete(request, snippet_id):
    if request.method == "POST" or request.method == "GET":
        snippet = get_object_or_404(Snippet.objects.filter(user = request.user), id=snippet_id)
        snippet.delete()
    return redirect("snippets-list")

def create_user(request):
    context = {'pagename': 'Регистрация нового пользователя',}
# Create empty form by GET method
    if request.method == "GET":
        form = UserRegistrationForm()
        context['form'] = form
        return render(request, 'pages/registration.html', context)

    if request.method =="POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        context['form'] = form
        return render(request,"pages/registration.html", context)   


def login(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       # print("username =", username)
       # print("password =", password)
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           context ={
               "pagemane": "PythonBin",
               "errors": ["wrong username or password",]
           }
           return render(request,"index.html",context)
   return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect("home")

@login_required
def comments_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get("snippet_id")
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author =  request.user
            comment.snippet = snippet
            comment.save()
            return redirect("snippet-detail", snippet_id = snippet.id)
    return HttpResponseNotAllowed(['POST'])    
