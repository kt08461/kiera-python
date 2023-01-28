from django.shortcuts import render

def crawler(request, page=10):
    from . import crawler

    return crawler.crawlerMain(request, page)

def students(request):
    from . import students

    return students.studentsMain(request)

def cifar10(request):
    from . import cifar10

    return cifar10.cifar10Main(request)

def cifar10_heroku(request):
    from . import cifar10_heroku

    return cifar10_heroku.cifar10Main(request)

def index(request):
    context = {}

    return render(request, "index.html", context)