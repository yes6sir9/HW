from reservations.models import Reservation
from django.shortcuts import render, redirect, get_object_or_404
from .models import Table
from .forms import TableForm


def table_list(request):
    booked_tables = Reservation.objects.values_list('table_id', flat=True)  
    tables = Table.objects.all()

    for table in tables:
        if table.id in booked_tables:
            table.is_available = False  
        else:
            table.is_available = True

    return render(request, 'tables/tables_list.html', {'tables': tables})

def available_tables(request):
    booked_tables = Reservation.objects.values_list('table_id', flat=True)  
    tables = Table.objects.exclude(id__in=booked_tables)  
    return render(request, 'tables/available_tables.html', {'tables': tables})



def add_table(request):
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tables_list')
    else:
        form = TableForm()
    return render(request, 'tables/add_table.html', {'form': form})


def edit_table(request, id):
    table = get_object_or_404(Table, id=id)
    if request.method == "POST":
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            return redirect('tables_list')
    else:
        form = TableForm(instance=table)
    return render(request, 'tables/edit_table.html', {'form': form})

def delete_table(request, id):
    table = get_object_or_404(Table, id=id)
    if request.method == "POST":
        table.delete()
        return redirect('tables_list')
    return render(request, 'tables/delete_table.html', {'table': table})
