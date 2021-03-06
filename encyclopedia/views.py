from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import markdown
import random

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
    search_entry_name = request.GET.get('q', '').lower()
    entry = util.get_entry(search_entry_name)
    if entry:
        return redirect(reverse('view_entry', args=[search_entry_name]))

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(search_entry_name),
        'search_entry_name': search_entry_name
    })


def create_entry(request: HttpRequest):
    if request.method == 'POST':
        title = request.POST['entry-title']
        content = request.POST['entry-content']
        errors = validate_new_entry(title, content)
        if len(errors['title']) or len(errors['content']):
            return render(request, 'encyclopedia/create_entry.html', {
                'errors': errors,
            })
        util.save_entry(title, content)
        return redirect(reverse('view_entry', args=[title]))

    edit = request.GET.get('edit')
    return render(request, 'encyclopedia/create_entry.html', {
        'edit_title': edit,
        'edit_content': util.get_entry(edit) if edit else None
    })


def random_entry(request: HttpRequest):
    return redirect(reverse('view_entry', args=[random.choice(util.list_entries())]))


def validate_new_entry(title, content):
    errors = {
        'title': [],
        'content': []
    }
    if not title:
        errors['title'].append('Title cannot be empty')
    if not content:
        errors['content'].append('Content cannot be empty')

    return errors
