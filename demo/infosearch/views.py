from django.shortcuts import render

from .Task5.main import read_inverted_index, load_file_names, vector_search


def index(request):
    search_query = request.GET.get('search', '')
    print(search_query)
    file_path = '../Task3/inverted_index.txt'
    index_path = '../Task1/index.txt'
    inverted_index = read_inverted_index(file_path)
    search_results = vector_search(search_query, inverted_index)
    index_to_links = load_file_names(index_path)

    db = {index_to_links[s]: a for s, a in search_results}
    db_sorted = sorted(db.items(), key=lambda item: item[1])[:10]

    context = {
        "websites": db_sorted,
    }

    return render(request, 'infosearch/index.html', context)
