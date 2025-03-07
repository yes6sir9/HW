from django.shortcuts import render
from .models import Customer

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customers_list.html', {'customers': customers})

def customer_detail(request, id):
    customer = Customer.objects.get(id=id)
    return render(request, 'customers/customer_detail.html', {'customer': customer})
