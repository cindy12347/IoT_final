from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent, TextSendMessage, TemplateSendMessage, PostbackAction, CarouselTemplate, CarouselColumn
import requests

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
    user_id = event.source.user_id
    # Send a carousel template with image and button in the FollowEvent
    send_cat_intro(event)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    if message_text == '廁所':
        # Send a carousel template with image and button in the MessageEvent
        send_cat_intro(event)

@handler.add(PostbackAction)
def handle_postback(event):
    data = event.postback.data
    if data == 'action=show_amount':
        # Respond with the result of left_cal when the user clicks "我要知道！"
        result = left_cal()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))

def send_cat_intro(event):
    # Send a carousel template introducing different cats
    carousel_template = CarouselTemplate(columns=[
        CarouselColumn(
            thumbnail_image_url='https://i.ibb.co/jL4LsGD/PDP-7-Prem-c8d51501-40f4-4c6f-9237-c520c11d8048-1120x1120.webp', 
            title='第一隻喵',
            text='我是喵仔',
            actions=[PostbackAction(label='了解更多', data='action=show_cat01')],
        ),
        CarouselColumn(
            thumbnail_image_url='https://images.pexels.com/photos/257532/pexels-photo-257532.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 
            title='第二隻喵',
            text='我是毛毛',
            actions=[PostbackAction(label='了解更多', data='action=show_cat02')],
        ),
        CarouselColumn(
            thumbnail_image_url='https://images.pexels.com/photos/1404819/pexels-photo-1404819.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1', 
            title='第三隻喵',
            text='我是嚕嚕',
            actions=[PostbackAction(label='了解更多', data='action=show_cat03')],
        ),
    ])
    template_message = TemplateSendMessage(
        alt_text='喵喵介紹',
        template=carousel_template
    )
    line_bot_api.reply_message(event.reply_token, template_message)

# Function to send cat01 details
def send_cat01(event):
    message_A = []
    message_A.append(TextSendMessage(text="我是喵仔"))
    message_A.append(ImageSendMessage(
        original_content_url="https://images.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        preview_image_url="https://images.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    ))
    line_bot_api.reply_message(event.reply_token, message_A)

# Function to send cat02 details
def send_cat02(event):
    message_A = []
    message_A.append(TextSendMessage(text="我是毛毛"))
    message_A.append(ImageSendMessage(
        original_content_url="https://images.pexels.com/photos/257532/pexels-photo-257532.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        preview_image_url="https://images.pexels.com/photos/257532/pexels-photo-257532.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    ))
    line_bot_api.reply_message(event.reply_token, message_A)

# Function to send cat03 details
def send_cat03(event):
    message_A = []
    message_A.append(TextSendMessage(text="我是嚕嚕"))
    message_A.append(ImageSendMessage(
        original_content_url="https://images.pexels.com/photos/1404819/pexels-photo-1404819.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
        preview_image_url="https://images.pexels.com/photos/1404819/pexels-photo-1404819.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    ))
    line_bot_api.reply_message(event.reply_token, message_A)

# New API endpoint
@app.route("/new_api", methods=['GET'])
def left_cal():
    headers = {'token': 'your_token', 'Content-type': 'application/json'}
    data1 = requests.get(url='', headers=headers)
    data2 = requests.get(url='', headers=headers)

    # Process the data and return the result
    result = "234083234"  # Replace this with your logic for processing the data
    return result

if __name__ == "__main__":
    app.run()
