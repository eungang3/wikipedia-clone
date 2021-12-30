from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
from django.shortcuts import redirect
import random
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="title", widget=forms.TextInput(attrs={'placeholder': 'Enter title', 'class':'title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Enter contents', 'class':'content'}), label="content")

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'content'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # check if the entry already exists
            entries = util.list_entries()
            for entry in entries:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/error.html", {
                        "message" : "Entry already Exists. Try editing the existing entry."
                    })
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:index"))
    else:
        return render(request, "encyclopedia/create.html", {
            "form" : NewEntryForm()
         })

def entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "message" : "Entry does not exist."
        })
    html_entry = markdown2.markdown(entry)
    return render(request, "encyclopedia/entry.html", {
        "title" : title,
        "entry" : html_entry
    })

def search(request):
    query = request.POST["q"].lower()
    entries = util.list_entries()
    matches = []
    for entry in entries:
        # if there's a perfect match, redirect to that entry
        if entry.lower() == query:
            return redirect('encyclopedia:entry', title=f'{query}')
        # check if query is entry's substring
        if query in entry.lower():
            matches.append(entry)
    # if there's no perfect match, show search result page        
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "matches":matches
    })

def get_random(request):
    entries = util.list_entries()
    random_index = random.randint(0, len(entries)-1)
    random_entry = entries[random_index]
    return redirect('encyclopedia:entry', title=f'{random_entry}')

def edit(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('encyclopedia:entry', title=f'{title}')
        else:
            return render(request,"encyclopedia/error.html", {
            'message' : 'An error occured. Try again.'
            })

    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "form" : EditEntryForm({'content': f'{content}'}),
        "content" : content,
        "title" : title
    })
