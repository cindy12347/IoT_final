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

#@handler.add(FollowEvent)
#def handle_follow(event):
#    user_id = event.source.user_id
#    content = f"這是現在旺宏館的衛生紙剩餘用量！"
#    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    if message_text == '廁所':
        # Send a carousel template with image and button
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.ibb.co/jL4LsGD/PDP-7-Prem-c8d51501-40f4-4c6f-9237-c520c11d8048-1120x1120.webp', 
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
        result = left_cal()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
        

@app.route("/new_api", methods=['GET'])
def left_cal():
    headers = {'token': 'YOUR_API_TOKEN', 'Content-type': 'application/json'}
    
    # Make API requests
    response1 = requests.get(url='https://smart-campus.kits.tw/api/api/sensors/DISTANCE/7e8a1261-56a2-4ffd-ac2c-b7a5a1934422', headers=headers)
    response2 = requests.get(url='https://smart-campus.kits.tw/api/api/sensors_in_timeinterval/DISTANCE/7e8a1261-56a2-4ffd-ac2c-b7a5a1934422/1704907260000/1704907350000', headers=headers)
    
    # Extract JSON content from responses
    data1 = response1.json()
    data2 = response2.json()
    
    # Extract values
    values = [item["value"] for item in data2["Items"]]
    
    # Convert values list to a string
    values_text = ', '.join(map(str, values))
    
    return response2.text

if __name__ == "__main__":
    app.run()
