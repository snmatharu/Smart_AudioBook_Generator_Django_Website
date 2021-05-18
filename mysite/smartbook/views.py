from django.http import HttpResponse
from django.shortcuts import render, redirect
from smartbook import templates
from django.core.files.storage import FileSystemStorage
import pdftotext
from gtts import gTTS
import os
from django.views.static import serve
from django.contrib import messages 

def home(request):
    return render(request, 'home.html')

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        pat="media/"+name
        filename = conversion(name,pat)
        context['url'] = fs.url(filename)
    return render(request, 'upload.html', context)
def conversion(name,pat):
    with open(pat, "rb") as f:
        pdf = pdftotext.PDF(f)
    for mytext in pdf:
        # print(mytext)
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("media/audio/smart audio book "+name+".mp3")
        filename="audio/smart audio book "+name+".mp3"
        return filename