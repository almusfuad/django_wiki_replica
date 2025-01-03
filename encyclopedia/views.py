from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry):
    mkd = util.get_entry(entry)
    html = util.convert_markdown_to_html(mkd)
    title = html[html.find("<h3>") + len("<h3>"):html.find("</h3>")]
    return render(request, "encyclopedia/entry_page.html", {
        'title': title,
        'content': html,
    })
    

def edit_page(request, entry):
    mkd = util.get_entry(entry)
    title = mkd[mkd.find("# ") + len("# "):mkd.find("\n")]
    if request.method == "GET":
        return render(request, "encyclopedia/edit_page.html", {
            'title': title,
            'content': mkd
        })
    
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry_page.html", {
            'title': title,
            'content': util.convert_markdown_to_html(content)
        })

