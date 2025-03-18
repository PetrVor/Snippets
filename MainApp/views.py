from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.forms import SnippetForm
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


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
            form.save()
            return redirect("snippets-list")
        return render(request,"pages/add_snippet.html", {'form': form})    


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
            'pagename': 'Просмотр сниппетов',
            'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id):
    context ={'pagename': 'просмотр сниппета'}
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:    
        return render(request,"pages/error.html", context | {"error" : f"Snippet with id:{snippet_id} not found!"}) 
    else:      
        context['snippet'] = snippet
        context["type"] = "view"
    return render(request,'pages/snippet_page.html', context)

def snippet_edit(request,snippet_id):
    pass

def snippet_delete(request, snippet_id):
    if request.method == "POST" or request.method == "GET":
        snippet = get_object_or_404(Snippet, id=snippet_id)
        snippet.delete()
    return redirect("snippets-list")
        



