from django.http import Http404
from django.shortcuts import render
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
