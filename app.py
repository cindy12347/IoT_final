from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent, TextSendMessage, TemplateSendMessage, PostbackEvent, ButtonsTemplate, PostbackAction, CarouselTemplate, CarouselColumn
import requests
import json

# Replace 'YOUR_CHANNEL_ACCESS_TOKEN' and 'YOUR_CHANNEL_SECRET' with your actual credentials
line_bot_api = LineBotApi('dOBtG5dEqkb/JWk1UrLxfpeXWH44gdDUj0yW/8labLdLY3+1s1DxhTOQ+FM6u/DSh7bVatXM6SgikLni/98A7aCMiiefbFZ790FbIqHl7FG47vgsDBJBqo49IXfhnx1Y6AUzXzFnpysZq/qtmKXOfQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c38f9d5ed556c8ebae0d0103dc89a738')

app = Flask(__name__)

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    carousel_template = CarouselTemplate(columns=[
            CarouselColumn( 
                title='想知道衛生紙的剩餘用量嗎！',
                text='肯定要的吧',
                actions=[
                    PostbackAction(label='我要知道！', data='action=show_amount'),
                ]
            )
        ])
    template_message = TemplateSendMessage(
        alt_text='衛生紙剩餘用量',
        template=carousel_template
    )
    line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    if message_text == '衛生紙':
        # Send a carousel template with image and button
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn( 
                title='想知道衛生紙的剩餘用量嗎！',
                text='肯定要的吧',
                actions=[
                    PostbackAction(label='我要知道！', data='action=show_amount'),
                ]
            )
        ])
        template_message = TemplateSendMessage(
            alt_text='衛生紙剩餘用量',
            template=carousel_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if data == 'action=show_amount':
        # Respond with the result of left_cal when the user clicks "我要知道！"
        response = left_cal()

        carousel_template = CarouselTemplate(columns=[
            CarouselColumn( 
                title='想知道衛生紙的剩餘用量嗎！',
                text='肯定要的吧',
                actions=[
                    PostbackAction(label='我要知道！', data='action=show_amount'),
                ]
            )
        ])
        template_message = TemplateSendMessage(
            alt_text='衛生紙剩餘用量',
            template=carousel_template
        )
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=f'目前的衛生紙剩餘用量為：{response}'), template_message])
        
        

@app.route("/new_api", methods=['GET'])
def left_cal():
    headers = {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJhY2hlbG9yXzA0IiwidXVpZCI6ImJmN2IyZGY2LWI4ODktNDNhMC1hYzhjLTE2YmJmYTFjNjkyNSIsIm5hbWUiOiJiYWNoZWxvcl8wNCIsImlhdCI6MTcwNDk0NDIxOSwiZXhwIjoxNzA1MDMwNjE5fQ.Vc3Aq_GNSOd1IOSRu0loRPO5wMFiQQ35oFe-VYgJ8G8', 'Content-type': 'application/json'}
    
    # Make API requests
    response1 = requests.get(url='https://smart-campus.kits.tw/api/api/sensors/DISTANCE/7e8a1261-56a2-4ffd-ac2c-b7a5a1934422', headers=headers)
    response2 = requests.get(url='https://smart-campus.kits.tw/api/api/sensors_in_timeinterval/DISTANCE/7e8a1261-56a2-4ffd-ac2c-b7a5a1934422/1704907260000/1704907350000', headers=headers)
    
    # Parse JSON response
    data2 = response2.json()

    # Extract values
    values = [item["value"] for item in data2["Items"]]
    
    # Convert values list to a string
    values_text = ', '.join(map(str, values))


    return response1.text

if __name__ == "__main__":
    app.run()
