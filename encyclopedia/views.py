from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util


def index(request):
    """
    Displays an unordered list of all entries available.
    """
    entries = util.list_entries()
    if request.method == "POST":
        result = []
        for entry in entries:
            if request.POST["q"] in entry:
                if request.POST["q"] == entry:
                    return HttpResponseRedirect(f"{entry}/")
                result.append(entry)
        return render(request, "encyclopedia/index.html", {
        "entries": result,
        "all": False,
        "query": request.POST["q"]
    })
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "all": True
    })

def titles(request, title):
    """
    Renders a page that displays the contents of the encyclopedia entry
    whose title is given in the URL. 
    Renders an error page if no such entry exists.
    """
    if title in util.list_entries():
        mdfile = util.get_entry(title)
        markdowner = Markdown()
        html = markdowner.convert(mdfile)
        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "title": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": title,
            "title": "Not found"
        })
    

