from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse 
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def titles(request, title):
    mdfile = util.get_entry(title)
    markdowner = Markdown()
    html = markdowner.convert(mdfile)
    return render(request, "encyclopedia/entry.html", {
        "entry": html
    })

