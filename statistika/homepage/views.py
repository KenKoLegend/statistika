from django.shortcuts import render, redirect
from .models import UploadedFile
import pandas as pd
from django.http import HttpResponse

def upload_file(request):
    if request.method == 'POST':
        
        uploaded_file = request.FILES['file']
        UploadedFile.objects.create(file=uploaded_file)
        
        return redirect('process_file')
    
    return render(request, 'uploaded_file.html')



def process_file(request):
    uploaded_file = UploadedFile.objects.latest('id')
    file_path = uploaded_file.file.path
    df = pd.read_excel(file_path, sheet_name=None)
    
    sum = []
    
    for sheet_name, sheet_data in df.items():
        try:
            wert_o11 = sheet_data.iloc[9, 14]
            sum.append({'Arbeitsblatt': sheet_name, 'Summe_O11': wert_o11})
        except KeyError:
            sum.append({'Arbeitsblatt': sheet_name, 'Summe_O11': 0})
    return render(request, 'process_file.html', {'sum': sum})
        