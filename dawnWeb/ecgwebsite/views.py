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

from linebot import LineBotApi
from linebot.models import TextSendMessage
tfmodel = tfmodels.load_model("ecgwebsite/testvaldata_model.h5")
# Create your views here.
def frontend(request):
    return render(request, "home.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')

# prevent CSRF wrong
def backend(request):
    records = models.ECGRecord.objects.all()
    return render(request, 'datadashboard.html',context={'records':records})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
@csrf_exempt
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
        path+=str(current_datetime).replace(':','')+".csv"
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
        return render(request, "websocketConnect.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def add(request):

    return render(request, "add.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/login/')
def analysis(request,rec_id):
    user = request.user
    rec_id = rec_id
    rec_name = models.ECGRecord.objects.get(id=rec_id).ecgrecord
    rec_name = str(rec_name).replace(':','')
    path=os.getcwd()+"/ECGRecord/"+str(user)+'/'+rec_name
    df = pd.read_csv(path)
    ECGdata = list(df['ECGdata'])
    
    print(ECGdata)
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


    time_domain_features = get_time_domain_features(rpeaks[0])
    print(time_domain_features["sdnn"])
    if time_domain_features["sdnn"]/10000<0.2:
        text="您的健康狀況不佳，檢測出阻滯及心律不整"
    elif time_domain_features["sdnn"]/10000>200:
        text="您的健康狀況不佳，檢測出阻滯及心律不整"
    else:
        text="您的健康狀況良好，無檢測出阻滯及心律不整"
    print(time_domain_features)

    

    lineBotAPI = LineBotApi('Q915Z4Su8P2PHAB9ytEU5Is//EOf4Sz307M+U6Cgyd441U+dWJfHsAwiUBydm4ruzjo8IqPxunYVIU52b0MA7VkOLTKlUf3bW4jx/U6+CjX0z9jizbcDfT/uDvbr/1qdTFTCZ3xtHI7oq6i41VxkfQdB04t89/1O/w1cDnyilFU=')
    myID = 'Ub902bc6c0fd0fe8604704b0baeb75d04'

    #傳訊息給特定的UserID
    lineBotAPI.push_message(myID, TextSendMessage(text="您的健康狀況不佳，檢測出阻滯及心律不整"))
    context = {"ECGdata":ECGdata,"filename":rec_name,"HR":HR,"peak":len(rpeaks[0]),"index":time_domain_features,"text":text}
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


# crudfun


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def delete_rec(request, rec_id):
    record = models.ECGRecord.objects.get(id = rec_id)
    record.delete()
    messages.success(request, "Record removed successfully !")
    return redirect('/backend')

@csrf_exempt
def test(request):
    return render(request, "websocketConnect.html")