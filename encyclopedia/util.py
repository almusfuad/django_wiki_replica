import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title.rstrip("\r")}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))



def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        title = title.rstrip("\r")
        f = default_storage.open(f"entries/{title}.md").read().decode("utf-8")
        return f
    except FileNotFoundError:
        return None
    


def convert_markdown_to_html(content):
    """
    Converts markdown content to HTML.
    """
    print(f"Attempting to retrieve entry: {content}")
    if content and isinstance(content, str):
        return re.sub(r'(?m)^(?!<h1>)(.+)$', r'<p>\1</p>',
                     re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>',
                            re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>',
                                re.sub(r'(?m)^\* (.+)$', r'<ul><li>\1</li></ul>',
                                       re.sub(r'(?m)^## (.+)$', r'<h2>\1</h2>',
                                            re.sub(r'(?m)^# (.+)$', r'<h1>\1</h1>\n<hr>', content))))))
    
    
