from .models import UploadedFile
import pandas as pd
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

# Defining Homepage and return index.html
def index(request):
    return render(request, 'index.html')

# Defining Upload Button
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']: 
        try:
            uploaded_file = request.FILES['file'] # defines the file
            fs = FileSystemStorage() # defubes tge FileSystemStorage
            filename = fs.save(uploaded_file.name, uploaded_file) # saves file in FileSystemStorage

            request.session['uploaded_file'] = fs.url(filename) # defines Session name
            request.session.set_expiry(60) # defines expiration of session to 60 seconds
            messages.success(request, 'File uploaded successfully!') # success message
            return redirect('process_file') # returns process_file.html

        except Exception as e:
            messages.error(request, f'Error uploading the file: {str(e)}') # defines error handling with str

    return render(request, 'uploaded_file.html') # returns the uploaded_file.html

# Dedfining delete file after session expires
def delete_file(request):
    
    uploaded_file_url = request.session.get('uploaded_file') 
    
    if uploaded_file_url:
        try:
            fs = FileSystemStorage() # declares fs as FileSystemStorage
            fs.delete(uploaded_file_url) 
            del request.session['uploaded_file']  # deletes requestet Session 'uploaded_file'
            messages.success(request, 'File deleted successfully!') # success message
        except Exception as e:
            messages.error(request, f'Error deleting the file: {str(e)}') # defines error handling with str

    return redirect('process_file') # returns process_file.html

def process_file(request):
    
    uploaded_file = UploadedFile.objects.latest('id') # gets latest object id
    file_path = uploaded_file.file.path # declares the file_path
    df = pd.read_excel(file_path, sheet_name=None) # gets file_path and sheet_name of excel data via pandas
    
    sum = [] # declares sum to for loop as list
    meeting = 0 # declares to for loop as integer
    interview = 0 # declares to for loop as integer
    event = 0 # declares to for loop as integer
    social = 0 # declares to for loop as integer
    vendor = 0 # declares to for loop as integer
    press = 0 # declares to for loop as integer
    vip = 0 # declares to for loop as integer
    
    for sheet_name, sheet_data in df.items(): # starting for loop to geht located excel cells with pandas
        try:
            
            wert_o11 = sheet_data.iloc[9, 14] # trying to get cell with Index 9, 14... etc.
            wert_p11 = sheet_data.iloc[9, 15]
            wert_q11 = sheet_data.iloc[9, 16]
            wert_r11 = sheet_data.iloc[9, 17]
            wert_s11 = sheet_data.iloc[9, 18]
            wert_t11 = sheet_data.iloc[9, 19]
            wert_u11 = sheet_data.iloc[9, 20]
            
    
            sum.append({'Arbeitsblatt': sheet_name}) # .append adds an item to end of list and creating template tags
            sum.append({'Summe_O11': wert_o11})
            sum.append({'Summe_P11': wert_p11})
            sum.append({'Summe_Q11': wert_q11})
            sum.append({'Summe_R11': wert_r11})
            sum.append({'Summe_S11': wert_s11})
            sum.append({'Summe_T11': wert_t11})
            sum.append({'Summe_U11': wert_u11})
            
            meeting += wert_o11 # giving wert_o11 + value for loop for total sum
            interview += wert_p11
            event += wert_q11
            social += wert_r11
            vendor += wert_s11
            press += wert_t11
            vip += wert_u11

            
        except KeyError:
            sum.append({'Arbeitsblatt': sheet_name, # error handling giving int Zero 
                        'Summe_O11': 0,
                        'Summe_P11': 0,
                        'Summe_Q11': 0,
                        'Summe_R11': 0,
                        'Summe_S11': 0,
                        'Summe_T11': 0,
                        'Summe_U11': 0})

        
    return render(request, 'process_file.html', {'sum': sum, # creating template tags
                                                 'meeting': meeting,
                                                 'interview': interview,
                                                 'event': event,
                                                 'social': social,
                                                 'vendor': vendor,
                                                 'press': press,
                                                 'vip': vip,
                                                })
        