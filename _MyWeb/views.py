from django.shortcuts import render

def crawler(request, page=10):
    from . import crawler

    return crawler.crawlerMain(request, page)

def students(request):
    from . import students

    return students.studentsMain(request)

def index(request):
    context = {}

    return render(request, "index.html", context)