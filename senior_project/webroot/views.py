from django.shortcuts import render


def welcome(request):
    template = "webroot/welcome.html"
    context = dict(title="Welcome")
    return render(request, template, context)


def about(request):
    template = "webroot/about.html"
    context = dict(title="About")
    return render(request, template, context)
