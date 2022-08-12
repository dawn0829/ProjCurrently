from lib2to3.pgen2 import token
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from requests import request
 
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import models
import base64

line_bot_api = LineBotApi('Q915Z4Su8P2PHAB9ytEU5Is//EOf4Sz307M+U6Cgyd441U+dWJfHsAwiUBydm4ruzjo8IqPxunYVIU52b0MA7VkOLTKlUf3bW4jx/U6+CjX0z9jizbcDfT/uDvbr/1qdTFTCZ3xtHI7oq6i41VxkfQdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser(settings.CHANNEL_SECRET)
 
global link_token_response

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')    
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  
                lineId = event.source.user_id # 獲取Userid
                print(lineId)
                #line_bot_api.push_message(lineId, TextSendMessage(text="今日測量:3次\n本月累積測量:3次\n今日\n心率:81\n心率變異指標(HRV):50 \n尚未發現任何阻滯及心律不整"))
                #link_token_response = line_bot_api.issue_link_token(lineId)
                print(event.message.text)
                if event.message.text == "signup":
                    link_token_response = line_bot_api.issue_link_token(lineId)
                    line_bot_api.push_message(lineId, TextSendMessage(text="http://10.10.131.171:8000/comfirmlogin/"+lineId+"/"+link_token_response.link_token))
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

@login_required(login_url='/login/')
def comfirm_login(request,lineid,token):
    user = request.user()
    user = User.objects.get(username = user)
        
    document = models.UserInfo(
        user = user,
        userLineId = lineid
    )
    nonce = base64.encode(lineid)
    document.save()
    return redirect("https://access.line.me/dialog/bot/accountLink?linkToken="+token+"&nonce="+nonce)