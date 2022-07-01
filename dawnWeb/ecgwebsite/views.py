from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from . import models
import pandas as pd
from django.contrib.auth.models import User

import os
import datetime

from tensorflow.keras import models as tfmodels
from biosppy.signals import ecg
from scipy.signal import resample
from hrvanalysis import get_time_domain_features
tfmodel = tfmodels.load_model("ecgwebsite/testvaldata_model.h5")
# Create your views here.
def frontend(request):
    return render(request, "home.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
@csrf_exempt
# prevent CSRF wrong
def backend(request):
    records = models.ECGRecord.objects.all()
    return render(request, 'datadashboard.html',context={'records':records})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def delete_rec(request, userid):
    record = models.ECGRecord.objects.get(id = userid)
    record.delete()
    messages.success(request, "Record removed successfully !")
    return redirect('/backend')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def detect(request):
    if request.method=="POST":
        user = request.user

        tasks = request.POST.getlist("tasks[]")
        df = pd.DataFrame(tasks, columns=["ECGdata"])
        path=os.getcwd()+"/ECGRecord/"+str(user)+'/'
        if not os.path.exists(path):
            os.mkdir(path)
            
        current_datetime = datetime.datetime.now()
        #save filename to database          
        path+=str(current_datetime)+".csv"
        df.to_csv(path, index=False)

        #to database
        user = User.objects.get(username = user)
        
        document = models.ECGRecord(
            user = user,
            ecgrecord = str(current_datetime)+".csv"
        )
        document.save()
        messages.success(request, "ECGRecord save success!")
        
        return JsonResponse({"tasks": tasks}) 
    else:
        return render(request, "DataVisual.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def add(request):

    return render(request, "add.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def analysispage(request):
    user = request.user
    path=os.getcwd()+"/ECGRecord/"+str(user)+'/'
    filename = "2022-05-27 03:31:18.376276.csv"
    print(models.ECGRecord.objects.all())
    df = pd.read_csv(path+filename)
    ECGdata = list(df['ECGdata'])
    
    
    fs = 360
    ecgre = df.values.reshape(len(df))
    ecgre = resample(ecgre,500*23)
    rpeaks = ecg.christov_segmenter(ecgre, sampling_rate=fs)

    HR = len(rpeaks[0])/22*60
    # wave,wpredict =[],[]
    # for i in range(len(rpeaks[0])):
    #     print(tfmodel.predict_classes(wave[i].reshape(1,250)))       
    #     wave.append(ecgre[rpeaks[0][i]-100:rpeaks[0][i]+150])
    #     wpredict.append(tfmodel.predict_classes(wave[i].reshape(1,250)))
    #MeanRR = 

    time_domain_features = get_time_domain_features(rpeaks[0])
    print(time_domain_features["sdnn"])
    if time_domain_features["sdnn"]/10000<0.2:
        text="您的健康狀況不佳，檢測出阻滯及心律不整"
    elif time_domain_features["sdnn"]/10000>200:
        text="您的健康狀況不佳，檢測出阻滯及心律不整"
    else:
        text="您的健康狀況良好，無檢測出阻滯及心律不整"
    print(time_domain_features)
    context = {"ECGdata":ECGdata,"filename":filename,"HR":HR,"peak":len(rpeaks[0]),"index":time_domain_features,"text":text}
    return render(request, "analysispage.html",context=context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def history(request):

    return render(request, "datadashboard.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def quiz(request):
    return render(request, "quiz.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def exercise(request):
    return render(request, "exercise.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def meditation(request):
    return render(request, "meditation.html")

def guide(request):
    return render(request, "intro/guide.html")

def usetool(request):
    return render(request, "intro/usetool.html")


