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
    


def calculate_similarity(query, entry):
    """
    Calculated a basic similarity score between two strings.
    """

    query = query.lower()
    entry = entry.lower()


    # Common characters between the query and the entry
    common_chars = set(query) & set(entry)      # Find the intersection of the two sets
    score = len(common_chars) / max(len(query), len(entry))


    print(f"Similarity score for {query} with {entry}: {score}")
    print(f"Common characters: {common_chars}")

    # Bonus for substring matching
    if query in entry or entry in query:
        score += 0.5

    return min(score, 1.0)


def search_entries(query):
    """
    Searches for entries that match the query string.
    """

    entries = list_entries()
    best_match = None
    highest_score = 0


    for entry in entries:
        similarity_score = calculate_similarity(query, entry)
        

        if similarity_score > highest_score:
            highest_score = similarity_score
            best_match = entry

    return best_match
