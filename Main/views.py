import csv
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from Main.models import DataEntry
from DBOperationTest.forms import UploadCSVForm
from datetime import datetime

def upload_csv(request):
    if request.method == "POST":
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            data = csv.reader(csv_file.read().decode('utf-8-sig').splitlines())

            conflicting_rows = []
            new_entries = []

            for row in data:
                unix_month = int(row[0])
                # Check for conflicts
                if DataEntry.objects.filter(unix_month=unix_month).exists():
                    conflicting_rows.append(row)
                else:
                    new_entries.append(row)

            if conflicting_rows:
                return JsonResponse({
                    'status': 'conflict',
                    'conflicting_rows': conflicting_rows,
                    'new_entries': new_entries
                })
            else:
                for row in new_entries:
                    DataEntry.objects.create(
                        unix_month=int(row[0]),
                        parameter_a=float(row[1]),
                        parameter_b=float(row[2]),
                        parameter_c=float(row[3]),
                        parameter_d=float(row[4]),
                        parameter_e=float(row[5]),
                        parameter_f=float(row[6]),
                        parameter_g=float(row[7]),
                        parameter_h=float(row[8])
                    )
                return JsonResponse({'status': 'success'})  # Return success status
    else:
        form = UploadCSVForm()
    return render(request, 'upload_csv.html', {'form': form})

def resolve_conflicts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get('action')
        conflicting_rows = data.get('conflicting_rows')
        new_entries = data.get('new_entries')

        if action == 'overwrite':
            # Handle overwriting
            DataEntry.objects.filter(unix_month__in=[int(row[0]) for row in conflicting_rows]).delete()
            for row in conflicting_rows:
                DataEntry.objects.create(
                    unix_month=int(row[0]),
                    parameter_a=float(row[1]),
                    parameter_b=float(row[2]),
                    parameter_c=float(row[3]),
                    parameter_d=float(row[4]),
                    parameter_e=float(row[5]),
                    parameter_f=float(row[6]),
                    parameter_g=float(row[7]),
                    parameter_h=float(row[8])
                )

        elif action == 'skip':
            # Handle skipping
            for row in new_entries:
                DataEntry.objects.create(
                    unix_month=int(row[0]),
                    parameter_a=float(row[1]),
                    parameter_b=float(row[2]),
                    parameter_c=float(row[3]),
                    parameter_d=float(row[4]),
                    parameter_e=float(row[5]),
                    parameter_f=float(row[6]),
                    parameter_g=float(row[7]),
                    parameter_h=float(row[8])
                )

        return JsonResponse({'status': 'success'})

def show_data(request):
    entries = DataEntry.objects.all().order_by('unix_month')
    return render(request, 'show_data.html', {'entries': entries})

def delete_row(request, id):
    if request.method == 'POST':
        try:
            entry = DataEntry.objects.get(id=id)
            entry.delete()
            messages.success(request, "刪除資料成功")
        except DataEntry.DoesNotExist:
            messages.error(request, "要刪除的資料不存在")
        return redirect('show_data')

def clear_data(request):
    if request.method == 'POST':
        DataEntry.objects.all().delete()
        messages.success(request, "已清空所有資料")
        return redirect('show_data')

def update_row(request, id):
    if request.method == 'POST':
        entry = DataEntry.objects.get(id=id)
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')

        if field == 'unix_month':
            date_obj = datetime.strptime(value, '%Y%m')
            unix_month = (date_obj.year - 1970) * 12 + date_obj.month - 1
            entry.unix_month = unix_month
        else:
            setattr(entry, field, float(value))

        entry.save()
        return JsonResponse({'status': 'success'})

def data_visualize(request):
    entries = DataEntry.objects.all().order_by('unix_month')

    labels = [entry.converted_date for entry in entries]
    data = [[entry.parameter_a for entry in entries],
            [entry.parameter_b for entry in entries],
            [entry.parameter_c for entry in entries],
            [entry.parameter_d for entry in entries],
            [entry.parameter_e for entry in entries],
            [entry.parameter_f for entry in entries],
            [entry.parameter_g for entry in entries],
            [entry.parameter_h for entry in entries]]

    return render(request, 'data_visualize.html', {
        'labels': labels,
        'data': data,
    })

# 基本的首頁視圖
def index(request):
    return render(request, 'base.html')