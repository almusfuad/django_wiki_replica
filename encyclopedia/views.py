from django.shortcuts import render
import re
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry):
    html = util.get_entry(entry)
    print(html)
    title = html[html.find("<h3>") + len("<h3>"):html.find("</h3>")]

    if request.method == "GET":
        return render(request, "encyclopedia/entry_page.html", {
            'title': title,
            'content': html
        })

