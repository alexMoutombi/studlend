from django.shortcuts import render

from apps.home.models import Loan

# Create your views here.

def investments(request):
    loans = Loan.objects.all()
    print(loans)
    return render(request, 'home/investments.html', context= {'loans': loans})