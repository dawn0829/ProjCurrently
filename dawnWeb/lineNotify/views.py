from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from requests import request
 
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage

line_bot_api = LineBotApi('Q915Z4Su8P2PHAB9ytEU5Is//EOf4Sz307M+U6Cgyd441U+dWJfHsAwiUBydm4ruzjo8IqPxunYVIU52b0MA7VkOLTKlUf3bW4jx/U6+CjX0z9jizbcDfT/uDvbr/1qdTFTCZ3xtHI7oq6i41VxkfQdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('156d13d42316e5f47696f65c96b8e528')
 
 
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
                
                line_bot_api.push_message(lineId, TextSendMessage(text="今日測量:3次\n本月累積測量:3次\n今日\n心率:81\n心率變異指標(HRV):50 \n尚未發現任何阻滯及心律不整"))
                

        return HttpResponse()
    else:
        return HttpResponseBadRequest()