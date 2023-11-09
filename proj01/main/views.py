from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def result_view(request) :
    if request.method == 'POST' :
        return render(request, 'main/result.html', {})










def temp_index(request):
    return render(request, 'main/temp_index.html', {})

def temp_result(request) :
    return render(request, 'main/temp_result.html', {})