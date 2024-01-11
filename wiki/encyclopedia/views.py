from django.shortcuts import render
from markdown2 import Markdown

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