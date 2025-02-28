from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from my_app import models
from .models import Account, Expense
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from datetime import datetime
from .forms import ExpenseForm


def home(request):
    return render(request, 'home/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {"form": form})  

class ExpensesListView(FormView):
    template_name = 'expenses/expenses_list.html'  
    form_class = ExpenseForm
    success_url = '/' 


