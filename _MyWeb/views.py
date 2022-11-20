from django.shortcuts import render

def crawler(request):
    from . import crawler

    return crawler.crawlerMain(request)

def students(request):
    from . import students

    return students.studentsMain(request)

def index(request):
    context = {}

    return render(request, "index.html", context)