import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from Main.models import DataEntry
from DBOperationTest.forms import UploadCSVForm
from datetime import datetime
from django.http import JsonResponse
import json

# 上傳 CSV 檔案的視圖
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

# 顯示資料的視圖
def show_data(request):
    entries = DataEntry.objects.all().order_by('unix_month')  # 按照 unix_month 排序
    return render(request, 'show_data.html', {'entries': entries})

# 刪除單列資料的視圖
def delete_row(request, id):
    if request.method == 'POST':  # 使用 POST 方法
        try:
            entry = DataEntry.objects.get(id=id)
            entry.delete()
            messages.success(request, "刪除資料成功")
        except DataEntry.DoesNotExist:
            messages.error(request, "要刪除的資料不存在")
        return redirect('show_data')

# 清空資料庫的視圖
def clear_data(request):
    if request.method == 'POST':
        DataEntry.objects.all().delete()  # 刪除所有資料
        messages.success(request, "已清空所有資料")
        return redirect('show_data')

# 更新單列資料的視圖
def update_row(request, id):
    if request.method == 'POST':
        entry = DataEntry.objects.get(id=id)
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')

        # 根據 field 來更新對應的欄位
        if field == 'unix_month':
            # 將 YYYYMM 轉換為 UNIX 月份
            from datetime import datetime
            date_obj = datetime.strptime(value, '%Y%m')
            unix_month = (date_obj.year - 1970) * 12 + date_obj.month - 1
            entry.unix_month = unix_month
        else:
            setattr(entry, field, float(value))  # 將數值欄位更新為浮點數

        entry.save()  # 保存更新
        return JsonResponse({'status': 'success'})  # 返回 JSON 響應

# 基本的首頁視圖
def index(request):
    return render(request, 'base.html')

#line_chart_test
def data_visualize(request):
    entries = DataEntry.objects.all().order_by('unix_month')

    # 提取數據給前端
    labels = [entry.converted_date for entry in entries]  # 這裡的 unix_month 是數字
    data = [[entry.parameter_a for entry in entries],
            [entry.parameter_b for entry in entries],
            [entry.parameter_c for entry in entries],
            [entry.parameter_d for entry in entries],
            [entry.parameter_e for entry in entries],
            [entry.parameter_f for entry in entries],
            [entry.parameter_g for entry in entries],
            [entry.parameter_h for entry in entries]]         # 對應的數據值

    return render(request, 'data_visualize.html', {
        'labels': labels,
        'data': data,
    })