from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from markdown2 import Markdown
from random import choice
from django.contrib.auth import login, logout, authenticate

from . import util
import encyclopedia

class NewEntry(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={"class":"form-control"}))
    content = forms.CharField(label="Content", widget=forms.Textarea(
        attrs={"class":"form-control"}))

class EditEntry(forms.Form):
    content = forms.CharField(label="Edit Content", widget=forms.Textarea(
        attrs={"class":"form-control"}))

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
        "search": True,
        "query": request.POST["q"]
    })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
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
                util.save_entry(title, content)
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

def edit(request):
    """
    Allows the user to edit a specific entry’s Markdown content.
    """
    if request.method == "GET":
        title = request.GET["title"]
        return render(request, "encyclopedia/edit.html", {
            "edit_entry": EditEntry(initial={"content": util.get_entry(title)}),
            "title": title
            })
    elif request.method == "POST":
        edited_entry = EditEntry(request.POST)
        if edited_entry.is_valid():
            title = request.POST["title"]
            content = edited_entry.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}/")
        else:
            return render(request, "encyclopedia/edit.html", {
            "edit_entry": edited_entry,
            "title": title
            })

def random(request):
    """
    Takes the user to a random encyclopedia entry.
    """
    title = choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{title}/")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        current_user = authenticate(request, username=username, password=password)
        if current_user is None:
            return render(request, "encyclopedia/login.html", {
                "message": "Invalid log in information."
            })
        else:
            login(request, current_user)
            return render(request, "encyclopedia/index.html", {
                "message": "Successfully logged in!",
                "entries": util.list_entries()
            })
    else:
        return render(request, "encyclopedia/login.html")

def logout_view(request):
    logout(request)
    return render(request, "encyclopedia/index.html", {
        "message": "Successfully logged out.",
        "entries": util.list_entries()
    })

    

