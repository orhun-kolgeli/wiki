from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from markdown2 import Markdown

from . import util
import encyclopedia

class NewEntry(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

class EditEntry(forms.Form):
    content = forms.CharField(label="Edit Content", widget=forms.Textarea)

def index(request):
    """
    Displays an unordered list of all entries available.
    """
    if request.method == "POST":
        result = []
        for entry in util.list_entries():
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
        "entries": util.list_entries(),
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

def create(request):
    """
    Allows the user to create a new encyclopedia entry.
    """
    if request.method == "POST":
        new_entry = NewEntry(request.POST)
        if new_entry.is_valid():
            title = new_entry.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/create.html", {
                    "new_entry": new_entry,
                    "entry_exists": True
                })
            else:
                content = new_entry.cleaned_data["content"]
                entry_file = open(f"entries/{title}.md", "w")
                for line in content:
                    entry_file.write(line)
                entry_file.close()
                return HttpResponseRedirect(f"/wiki/{title}/")
        else:
            return render(request, "encyclopedia/create.html", {
                "new_entry": new_entry,
                "entry_exists": False
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "new_entry": NewEntry(),
            "entry_exists": False
        })
    

