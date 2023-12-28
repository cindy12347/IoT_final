from flask import Flask, request, abort, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FollowEvent, TextSendMessage
import requests

# Replace 'YOUR_CHANNEL_ACCESS_TOKEN' and 'YOUR_CHANNEL_SECRET' with your actual credentials
line_bot_api = LineBotApi('dOBtG5dEqkb/JWk1UrLxfpeXWH44gdDUj0yW/8labLdLY3+1s1DxhTOQ+FM6u/DSh7bVatXM6SgikLni/98A7aCMiiefbFZ790FbIqHl7FG47vgsDBJBqo49IXfhnx1Y6AUzXzFnpysZq/qtmKXOfQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c38f9d5ed556c8ebae0d0103dc89a738')

app = Flask(__name__)

@app.route("/", methods=['POST'])  # Change the route to handle POST requests to "/"
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def tissuepaper ():
    content = 345
    return content

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    if message_text == '廁所':
        content=tissuepaper()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))

@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    content = f"這是我們物聯網概論的期末project!謝謝你訂閱我們！"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))

# New API endpoint
@app.route("/new_api", methods=['GET'])
def new_api():
    # Example of making a request to another API (https://smart-campus.kits.tw/)
    headers = {'token':eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJhY2hlbG9yXzA0IiwidXVpZCI6ImJmN2IyZGY2LWI4ODktNDNhMC1hYzhjLTE2YmJmYTFjNjkyNSIsIm5hbWUiOiJiYWNoZWxvcl8wNCIsImlhdCI6MTcwMzc3NTE0MiwiZXhwIjoxNzAzODYxNTQyfQ.ziyY8dJJZ0loGlok7uI60JmzyjkmJtb96GN_oN-u6rk, 'Content-type':'application/json'}
    data1 = requests.get(url='', headers=headers)
    data2 = requests.get(url='', headers=headers)
    data1 = "not known"
    data2 = "not known"

    # Check if the request was successful
    #if data1.status_code == 200 & data2.status_code == 200:
    #    
    #else:

    return data1

def tissuepaper ():
    content = new_api()
    return content

if __name__ == "__main__":
    app.run()
