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
            wert_p11 = sheet_data.iloc[9, 15]
            wert_q11 = sheet_data.iloc[9, 16]
            wert_r11 = sheet_data.iloc[9, 17]
            wert_s11 = sheet_data.iloc[9, 18]
            wert_t11 = sheet_data.iloc[9, 19]
            wert_u11 = sheet_data.iloc[9, 20]
            
    
            sum.append({'Arbeitsblatt': sheet_name})
            sum.append({'Summe_O11': wert_o11} )
            sum.append({'Summe_P11': wert_p11})
            sum.append({'Summe_Q11': wert_q11})
            sum.append({'Summe_R11': wert_r11})
            sum.append({'Summe_S11': wert_s11})
            sum.append({'Summe_T11': wert_t11})
            sum.append({'Summe_U11': wert_u11})
        except KeyError:
            sum.append({'Arbeitsblatt': sheet_name, 'Summe_O11': 0})
        
    return render(request, 'process_file.html', {'sum': sum})
        