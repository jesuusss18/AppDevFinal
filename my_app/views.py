from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from my_app import models
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.views.generic import TemplateView
from django.template.loader import render_to_string
from django.views.generic.edit import FormView
from .models import Account, Liability
from .forms import LiabilityForm
from .utils import generate_graph
import plotly.express as px

# Render the home page
def home(request):
    return render(request, 'home/home.html')

# Register new user and log them in
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Handle expense form and display list of liabilities
class ExpenseListView(FormView):
    template_name = 'expenses/expense_list.html'
    form_class = LiabilityForm
    success_url = '/'

    # Save liability and return updated data as JSON if Ajax request
    def form_valid(self, form):
        account, _ = Account.objects.get_or_create(user=self.request.user)

        liability = Liability(
            name=form.cleaned_data['name'],
            amount=form.cleaned_data['amount'],
            interest_rate=form.cleaned_data['interest_rate'],
            date=form.cleaned_data['date'],
            end_date=form.cleaned_data['end_date'],
            long_term=form.cleaned_data['long_term'],
            user=self.request.user
        )
        liability.save()

        account.liability_list.add(liability)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            liability_html = f"""
            <div class="expense-item" id="expense-{liability.id}">
                <h4>{liability.name}</h4>
                <p>Amount: {liability.amount}</p>
                <p>Monthly Expense: {liability.monthly_expense}</p>
                <p>Due Date: {liability.date}</p>
                <p>End Date: {liability.end_date}</p>
            </div>
            """
            graph_data = self.get_graph_data()

            return JsonResponse({
                'success': True,
                'html': liability_html,
                'graphData': graph_data
            })

        return super().form_valid(form)

    # Get graph data to visualize expenses
    def get_graph_data(self):
        aggregated_data = self.aggregate_expenses()
        graph_data = {
            'months': [item['year_month'] for item in aggregated_data],
            'expenses': [item['expenses'] for item in aggregated_data]
        }
        graph_data['chart'] = generate_graph(graph_data)
        return graph_data

    # Aggregate expenses by month
    def aggregate_expenses(self):
        expense_data_graph = {}
        for account in Account.objects.filter(user=self.request.user):
            liabilities = account.liability_list.all()
            for liability in liabilities:
                year_month = liability.date.strftime('%Y-%m')
                if year_month not in expense_data_graph:
                    expense_data_graph[year_month] = []
                expense_data_graph[year_month].append({
                    'name': liability.name,
                    'amount': liability.monthly_expense if liability.long_term else liability.amount,
                    'date': liability.date,
                })

        aggregated_data = [{'year_month': key, 'expenses': sum(item['amount'] for item in value)}
                           for key, value in expense_data_graph.items()]

        return aggregated_data

    # Add expenses and graph data to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expense_data'] = self.get_expenses_data()
        context['graph_data'] = self.get_graph_data()['chart']
        return context

    # Get expense data grouped by month
    def get_expenses_data(self):
        expense_data = {}
        for account in Account.objects.filter(user=self.request.user):
            liabilities = account.liability_list.all()
            for liability in liabilities:
                year_month = liability.date.strftime('%Y-%m')
                if year_month not in expense_data:
                    expense_data[year_month] = []
                expense_data[year_month].append({
                    'name': liability.name,
                    'amount': liability.monthly_expense if liability.long_term else liability.amount,
                    'date': liability.date,
                })
        return expense_data

