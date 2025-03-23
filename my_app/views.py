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

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.views.generic import TemplateView
from .models import Account, Liability
from .forms import Expense, ExpenseForm
from django.views.generic.edit import FormView
from django.views.generic import ListView
from django.utils.safestring import mark_safe
from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px
from plotly.graph_objs import *


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

    def form_valid(self, form):
        account, _ = Account.objects.get_or_create(user=self.request.user)
        
        expense = Expense(
            name=form.cleaned_data['name'],
            amount=form.cleaned_data['amount'],
            interest_rate=form.cleaned_data['interest_rate'],
            date=form.cleaned_data['date'],
            end_date=form.cleaned_data['end_date'],
            long_term=form.cleaned_data['long_term'],
            user=self.request.user
        )
        expense.save()
        account.expenses_list.add(expense)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        accounts = Account.objects.filter(user=user)
        expense_data_graph = {}
        expense_data = {}

        for account in accounts:
            expense = account.expenses_list.all()
            for expense in account.expenses_list,all():
                if expense.long_term and expense.monthly_expense:
                    current_date = expense.date
                    while current_date <= expense.end_date:
                        year_month = current_date.strftime('%Y-%m')
                        if year_month not in expense_data_graph:
                            expense_data_graph[year_month] = []

                        expense_data_graph[year_month].append({
                            'name': expense.name,
                            'amount': expense.monthly_expense,
                            'date': expense.date,
                            'end_date': expense.end_date,
                        })

                        # Move to the next month
                        current_date = current_date + relativedelta(months=1)
                else:
                    year_month = expense.date.strftime('%Y-%m')
                    if year_month not in expense_data_graph:
                        expense_data_graph[year_month] = []

                    expense_data_graph[year_month].append({
                        'name': expense.name,
                        'amount': expense.amount,
                        'date': expense.date,
                    })               

        for account in accounts:
            expense = account.expenses_list.all()
            for expense in account.expenses_list.all():
                if expense.long_term and expense.monthly_expense:
                    current_date = expense.date
                    year_month = current_date.strftime('%Y-%m')
                    if year_month not in expense_data:
                        expense_data[year_month] = []

                    expense_data[year_month].append({
                        'name': expense.name,
                        'amount': expense.monthly_expense,
                        'date': expense.date,
                        'end_date': expense.end_date,
                        'long_term': expense.long_term,
                    })

                        # Move to the next month
                    current_date = current_date + relativedelta(months=1)
                else:
                    year_month = expense.date.strftime('%Y-%m')
                    if year_month not in expense_data:
                        expense_data[year_month] = []

                    expense_data[year_month].append({
                        'name': expense.name,
                        'amount': expense.amount,
                        'date': expense.date,
                    })              
        # Convert the expense_data_graph into aggregated_data
        aggregated_data = [{'year_month': key, 'expenses': sum(item['amount'] for item in value)} for key, value in expense_data_graph.items()]

        context['expense_data'] = expense_data
        context['aggregated_data'] = aggregated_data

        # Prepare graph_data for generating the Plotly graph





