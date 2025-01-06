from django.shortcuts import render, redirect

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry):
    mkd = util.get_entry(entry)
    html = util.convert_markdown_to_html(mkd)

    title = mkd[mkd.find("# ")+len("# "):mkd.find("\n")]
    
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
    

def create_new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create_new_page.html")


    if request.method == "POST":
        # Get the title and content from the form
        title = request.POST.get('title')
        content = request.POST.get('content')


        # check if an entry with the same title already exists
        if util.get_entry(title):
            return render(request, "encyclopedia/create_new_page.html", {
                'error': 'An entry with the same title already exists'
            })

        # Save the entry
        markdown_content = f"# {title}\n{content}"
        util.save_entry(title, markdown_content)

        # Redirect to the entry page
        return redirect('entry_page', entry=title)
    




