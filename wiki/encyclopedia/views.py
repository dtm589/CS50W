from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util

#function to convert md to html
def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html = convert_md_to_html(title)
    if html == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist, yet!"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "html" : html
        })
        
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html = convert_md_to_html(entry_search)
        if html is not None:
            return render(request, "encyclopedia/entry.html", {
                "title" : entry_search,
                "html" : html
            })
        else:
            all_entries = util.list_entries()
            recommedation = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recommedation.append(entry)
            return render(request, "encyclopedia/recommended.html", {
                "recommedation" : recommedation
            })
            
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        md = request.POST['md']
        title_exist = util.get_entry(title)
        if title_exist is not None:
            return render(request, "encyclopedia/error.html", {
                "message" : "An entry with this title already exisits!"
            })
        else:
            util.save_entry(title, md)
            html = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title" : title,
                "html" : html
            })
            
def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        html = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title" : title,
            "html" : html
        })
        
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['md']
        util.save_entry(title, content)
        html = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "html" : html
        })
        
def rand(request):
    all_entries = util.list_entries()
    random_entry = random.choice(all_entries)
    html = convert_md_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title" : random_entry,
        "html" : html
    })