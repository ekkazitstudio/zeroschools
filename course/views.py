from django.shortcuts import render

def index(request):
	return render(request, 'course/index.html')

def detail(request, slug):
	return render(request, 'course/detail.html')
