from django.shortcuts import render


# Create your views here.
def retorno(request):

    return render(request, 'pruebita.html')