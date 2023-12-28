from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, CarouselTemplate, CarouselColumn

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

def tissuepaper():
    content = 'not known'
    return content

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    if message_text == '廁所':
        content = tissuepaper()
        # Send a carousel template with image and button
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
                thumbnail_image_url='https://ibb.co/2jKjHPd',  # Replace with your image URL
                title='想知道現在衛生紙的剩餘用量嗎！',
                text='肯定要的吧',
                actions=[
                    PostbackAction(label='我要知道！', data='action=buy&itemid=1'),
                ]
            )
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel Template',
            template=carousel_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    content = f"這是現在旺宏館的衛生紙剩餘用量！"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))

# New API endpoint
@app.route("/new_api", methods=['GET'])
def new_api():
    headers = {'token': 'your_token', 'Content-type': 'application/json'}
    data1 = requests.get(url='', headers=headers)
    data2 = requests.get(url='', headers=headers)
    data1 = "not known"
    data2 = "not known"

    return data1

if __name__ == "__main__":
    app.run()
