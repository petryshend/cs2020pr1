from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def view_entry(request, entry_name):
    entry_content = util.get_entry(entry_name)
    if not entry_content:
        raise Http404('Entry does not exists')
    return render(request, 'encyclopedia/view_entry.html', {
        'entry_name': entry_name,
        'entry_content': markdown(entry_content)
    })


def search_entry(request: HttpRequest):
    search_entry_name = request.POST['q'].lower()
    entry = util.get_entry(search_entry_name)
    if entry:
        return redirect(reverse('view_entry', args=[search_entry_name]))

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(search_entry_name),
        'search_entry_name': search_entry_name
    })