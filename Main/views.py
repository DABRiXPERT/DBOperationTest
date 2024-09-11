import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from Main.models import DataEntry
from DBOperationTest.forms import UploadCSVForm

# Create your views here.
def upload_csv(request):
    if request.method == "POST":
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            data = csv.reader(csv_file.read().decode('utf-8-sig').splitlines())
            for row in data:
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
            messages.success(request, "上傳並寫入資料庫完成")
            return redirect('show_data')
    else:
        form = UploadCSVForm()
    return render(request, 'upload_csv.html', {'form': form})

def show_data(request):
    data = DataEntry.objects.all().order_by('unix_month')
    return render(request, 'show_data.html', {'data': data})

def delete_data(request):
    if request.method == "POST":
        date_str = request.POST.get('delete_dates')
        dates = date_str.split()
        for date in dates:
            year = int(date[:4])
            month = int(date[4:])
            unix_month = (year - 1970) * 12 + (month - 1)
            DataEntry.objects.filter(unix_month=unix_month).delete()
        messages.success(request, "刪除資料完成")
        return redirect('show_data')
    return render(request, 'delete_data.html')

def clear_data(request):
    if request.method == "POST":
        DataEntry.objects.all().delete()
        messages.success(request, "清除所有資料完成")
        return redirect('show_data')
    return render(request, 'clear_data.html')

def index(request):
    return render(request, 'base.html')
