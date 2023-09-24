from django.shortcuts import render, redirect
from .models import UploadedFile
import pandas as pd

def upload_file(request):
    if request.method == 'POST':
        
        uploaded_file = request.FILES['file']
        UploadedFile.objects.create(file=uploaded_file)
        
        return redirect('process_file')
    
    return render(request, 'uploaded_file.html')



def process_file(request):
    uploaded_file = UploadedFile.objects.latest('id')
    file_path = uploaded_file.file.path
    df = pd.read_excel(file_path)
    
    cell_value1 = df.iloc[0, 0]
    cell_value2 = df.iloc[0, 1]
    
    context = {
        "cell_value1": cell_value1,
        "cell_value2": cell_value2,
    }
    
    return render(request, 'process_file.html', context)
    